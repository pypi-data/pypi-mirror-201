# Copyright 2020-2023 Deere & Company.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from requests import HTTPError
import pytest


from security_scan_invoker.build_details_fetcher import BuildDetailsFetcher
from security_scan_invoker.build_details import BuildDetails
from .fake_veracode_api import FakeVeracodeAPI


class TestBuildDetailsFetcher:

    app_name = "my_app"
    app_id = "5067"
    status = "Pre-Scan Success"
    version = "GIT HASH"
    build_details = BuildDetails(status, version, app_id)
    build_info_content = (
        '<buildinfo app_id="5067"><build version="'
        + version
        + '"><analysis_unit analysis_type="Static" status="'
        + status
        + '"/></build></buildinfo>'
    )

    @pytest.fixture
    def veracode_api(self):
        my_app = {"app_id": self.app_id, "app_name": self.app_name}
        return FakeVeracodeAPI([my_app], self.build_info_content)

    def test_get_build_status_gets_app_list_and_build_info_when_app_exists(
        self, veracode_api
    ):
        BuildDetailsFetcher(veracode_api).get_build_details(self.app_name)

        assert veracode_api.got_app_list
        assert veracode_api.app_id_received == self.app_id

    def test_get_build_status_gets_build_info_when_more_than_one_app_in_list(self):
        my_app = {"app_id": self.app_id, "app_name": self.app_name}
        other_app = {"app_id": "34589", "app_name": "other_app"}
        veracode_api = FakeVeracodeAPI([other_app, my_app], self.build_info_content)

        BuildDetailsFetcher(veracode_api).get_build_details(my_app["app_name"])

        assert veracode_api.app_id_received == my_app["app_id"]

    @staticmethod
    def test_get_build_status_exits_when_app_cant_find_app(veracode_api):
        with pytest.raises(SystemExit) as exit_error:
            BuildDetailsFetcher(veracode_api).get_build_details("app_not_in_list")
        assert exit_error.value.code == str(
            "ERROR: Can't find app called app_not_in_list in any"
            + " of the 1 apps associated with your ID and Key."
        )

    def test_get_build_status_exits_when_cant_get_app_list(self, veracode_api):
        with pytest.raises(HTTPError):
            veracode_api.get_app_list_status_code = 400
            BuildDetailsFetcher(veracode_api).get_build_details(self.app_name)

    def test_get_build_status_returns_correct_status_version(self, veracode_api):
        build_details_returned = BuildDetailsFetcher(veracode_api).get_build_details(
            self.app_name
        )
        assert build_details_returned.status == self.build_details.status
        assert build_details_returned.version == self.build_details.version
        assert build_details_returned.app_id == self.build_details.app_id

    def test_get_build_status_exits_when_veracode_build_info_call_fails(
        self, veracode_api
    ):
        with pytest.raises(HTTPError):
            veracode_api.get_build_info_status_code = 400
            BuildDetailsFetcher(veracode_api).get_build_details(self.app_name)

    def test_delete_build_info_exits_when_veracode_delete_build_info_call_is_non_200_unsuccessful(
        self, veracode_api
    ):
        with pytest.raises(SystemExit):
            veracode_api.delete_build_info_status_code = 400
            BuildDetailsFetcher(veracode_api).delete_build_info(self.app_id)

    def test_delete_build_info_when_veracode_delete_build_info_call_is_successful(
        self, veracode_api
    ):
        BuildDetailsFetcher(veracode_api).delete_build_info(self.app_id)
        assert veracode_api.app_id_received == self.app_id

    def test_delete_build_info_exits_when_veracode_delete_build_info_call_throws_exception(
        self, veracode_api
    ):
        with pytest.raises(SystemExit) as exit_error:
            veracode_api.should_throw_error_delete_build = True
            BuildDetailsFetcher(veracode_api).delete_build_info(self.app_id)
        assert (
            "ERROR:"
            in exit_error.value.args[0]
        )

    def test_delete_build_info_parses_valid_response_content(
        self, veracode_api
    ):
        veracode_api.delete_build_content = {"deletebuildresult": {"result": "success"}}
        result = BuildDetailsFetcher(veracode_api).delete_build_info(self.app_id)
        assert result == "Delete completed successfully with status: success"

    def test_delete_build_info_parses_response_with_no_result(
        self, veracode_api
    ):
        veracode_api.delete_build_content = {"deletebuildresult":
                                             {"somethingelse": "notvalidresult"}}
        result = BuildDetailsFetcher(veracode_api).delete_build_info(self.app_id)
        assert "Delete call completed but did not list a result:" in result

    def test_delete_build_info_returns_error_string_when_response_content_is_null(
        self, veracode_api
    ):
        result = BuildDetailsFetcher(veracode_api).delete_build_info(self.app_id)
        assert "Unable to parse delete_build_info content." in result

    def test_delete_build_info_content_contains_error_field(
        self, veracode_api
    ):
        veracode_api.delete_build_content = {"error": "some error"}
        result = BuildDetailsFetcher(veracode_api).delete_build_info(self.app_id)
        assert result == "Error in running Delete: some error"

    def test_delete_build_info_content_has_empty_response(
        self, veracode_api
    ):
        veracode_api.delete_build_content = {"someval": "someotherval"}
        result = BuildDetailsFetcher(veracode_api).delete_build_info(self.app_id)
        assert "Delete call completed but did not list a valid result" in result
