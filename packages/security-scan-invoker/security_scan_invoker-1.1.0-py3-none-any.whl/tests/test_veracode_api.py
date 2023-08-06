# Copyright 2022-2023 Deere & Company.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
from unittest.mock import patch, mock_open
import mock
import pytest
import requests

from security_scan_invoker.veracode_api_wrapper import VeracodeAPIWrapper
from tests.fakes import FakeResponse, \
    FAKE_UPLOAD_FILE_SCAN_ALREADY_RUNNING, FAKE_UPLOAD_FILE_SUCCESS, FAKE_UPLOAD_FILE_FAILED, \
    FAKE_BEGIN_PRESCAN_SUCCESS, FAKE_BEGIN_PRESCAN_FAILED, \
    FAKE_GET_PRESCAN_NOT_AVAIL, FAKE_GET_PRESCAN_SUCCESS, \
    FAKE_BEGIN_SCAN_SUCCESS, FAKE_BEGIN_SCAN_ERROR


@pytest.fixture(name="fake_api_wrapper")
def mock_api_wrapper() -> VeracodeAPIWrapper:
    api = VeracodeAPIWrapper("test", "test")
    return api


@pytest.fixture(name="patched_sleep", autouse=True)
def mock_time_sleep():
    with mock.patch.object(time, "sleep") as mocked_time_sleep:
        yield mocked_time_sleep


class TestVeracodeAPIWrapper():

    @staticmethod
    @mock.patch.object(requests, "post")
    def test_upload_file_opens_file(patched_post):
        fake_resp = FakeResponse(200, FAKE_UPLOAD_FILE_SUCCESS)
        patched_post.return_value = fake_resp
        with patch("builtins.open", mock_open(read_data="data")) as mock_file:
            api = VeracodeAPIWrapper("test", "test")
            result = api.upload_file("test_app_id", "somefilepath")
            assert result
        mock_file.assert_called_with("somefilepath", "rb")

    @staticmethod
    @mock.patch.object(requests, "post")
    def test_upload_file_logs_and_throws_httperror(patched_post):
        fake_resp = FakeResponse(500, "")
        patched_post.return_value = fake_resp
        with pytest.raises(requests.HTTPError) as _error_http:
            with patch("builtins.open", mock_open(read_data="data")) as _mock_file:
                api = VeracodeAPIWrapper("test", "test")
                result = api.upload_file("test_app_id", "somefilepath")
                assert not result

    @staticmethod
    @mock.patch.object(requests, "post")
    def test_upload_file_scan_already_running(patched_post, caplog):
        fake_resp = FakeResponse(200, FAKE_UPLOAD_FILE_SCAN_ALREADY_RUNNING)
        patched_post.return_value = fake_resp
        with patch("builtins.open", mock_open(read_data="data")) as _mock_file:
            api = VeracodeAPIWrapper("test", "test")
            result = api.upload_file("test_app_id", "somefilepath")
            assert not result
        assert "Not in a state where file upload can occur" in caplog.text

    @staticmethod
    @mock.patch.object(requests, "post")
    def test_upload_file_unsuccessful_upload(patched_post, caplog):
        fake_resp = FakeResponse(200, FAKE_UPLOAD_FILE_FAILED)
        patched_post.return_value = fake_resp
        with patch("builtins.open", mock_open(read_data="data")) as _mock_file:
            api = VeracodeAPIWrapper("test", "test")
            result = api.upload_file("test_app_id", "somefilepath")
            assert not result
        assert "Unsuccessful upload of file" in caplog.text

    @staticmethod
    @mock.patch.object(requests, "get")
    def test_begin_prescan_successful(patched_get, fake_api_wrapper):
        fake_resp = FakeResponse(200, FAKE_BEGIN_PRESCAN_SUCCESS)
        patched_get.return_value = fake_resp
        assert fake_api_wrapper.begin_prescan("test_app_id")

    @staticmethod
    @mock.patch.object(requests, "get")
    def test_begin_prescan_build_status_fails(patched_get, fake_api_wrapper):
        fake_resp = FakeResponse(200, FAKE_BEGIN_PRESCAN_FAILED)
        patched_get.return_value = fake_resp
        assert not fake_api_wrapper.begin_prescan("test_app_id")

    @staticmethod
    @mock.patch.object(requests, "get")
    def test_begin_prescan_throws_httperror(patched_get, fake_api_wrapper):
        fake_resp = FakeResponse(500, FAKE_BEGIN_PRESCAN_SUCCESS)
        patched_get.return_value = fake_resp
        with pytest.raises(requests.HTTPError) as _error_http:
            fake_api_wrapper.begin_prescan("test_app_id")

    @staticmethod
    @mock.patch.object(requests, "get")
    def test_get_prescan_results_success(patched_get, fake_api_wrapper, patched_sleep):
        fake_resp = FakeResponse(200, FAKE_GET_PRESCAN_SUCCESS)
        patched_get.return_value = fake_resp
        assert fake_api_wrapper.get_prescan_results("test_app_id")
        assert patched_sleep.call_count == 0

    @staticmethod
    @mock.patch.object(requests, "get")
    def test_get_prescan_results_not_available(
            patched_get, fake_api_wrapper, patched_sleep, caplog):
        fake_resp = FakeResponse(200, FAKE_GET_PRESCAN_NOT_AVAIL)
        patched_get.return_value = fake_resp
        assert not fake_api_wrapper.get_prescan_results("test_app_id")
        assert "Unable to complete pre-scan." in caplog.text
        assert patched_sleep.call_count == 9

    @staticmethod
    @mock.patch.object(requests, "get")
    def test_get_prescan_results_raises_httperror(patched_get, fake_api_wrapper, patched_sleep):
        fake_resp = FakeResponse(500, FAKE_BEGIN_PRESCAN_SUCCESS)
        patched_get.return_value = fake_resp
        with pytest.raises(requests.HTTPError) as _error_http:
            fake_api_wrapper.get_prescan_results("test_app_id")
        assert patched_sleep.call_count == 0

    @staticmethod
    @mock.patch.object(requests, "get")
    def test_begin_scan_success(patched_get, fake_api_wrapper):
        fake_resp = FakeResponse(200, FAKE_BEGIN_SCAN_SUCCESS)
        patched_get.return_value = fake_resp
        assert fake_api_wrapper.begin_scan("test_app_id", False)

    @staticmethod
    @mock.patch.object(requests, "get")
    def test_begin_scan_fails(patched_get, fake_api_wrapper):
        fake_resp = FakeResponse(200, FAKE_BEGIN_SCAN_ERROR)
        patched_get.return_value = fake_resp
        assert not fake_api_wrapper.begin_scan("test_app_id", False)

    @staticmethod
    @mock.patch.object(requests, "get")
    def test_begin_scan_raises_httperror(patched_get, fake_api_wrapper):
        fake_resp = FakeResponse(500, FAKE_BEGIN_SCAN_SUCCESS)
        patched_get.return_value = fake_resp
        with pytest.raises(requests.HTTPError) as _error_http:
            fake_api_wrapper.begin_scan("test_app_id", False)

    @staticmethod
    @mock.patch.object(requests, "get")
    def test_begin_scan_selects_previous_modules_and_defaults(patched_get, fake_api_wrapper):
        fake_resp = FakeResponse(200, FAKE_BEGIN_SCAN_SUCCESS)
        patched_get.return_value = fake_resp
        assert fake_api_wrapper.begin_scan("test_app_id", False)
        assert "scan_all_top_level_modules" in patched_get.call_args[1]["params"]

        assert fake_api_wrapper.begin_scan("test_app_id", True)
        assert "select_previous_modules" in patched_get.call_args[1]["params"]
