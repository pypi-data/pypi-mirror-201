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

from security_scan_invoker.build_details import BuildDetails


class TestBuildDetails:
    @staticmethod
    def test_build_details_returns_app_id_if_no_status(caplog):
        test_data = {"buildinfo": {
            "@app_id": "test_app_id",
            "build": {
                "@version": "test_version"
            }
        }}
        result = BuildDetails.parse_build_details(test_data)
        assert result.app_id == "test_app_id"
        assert result.version != "test_version"
        assert not result.status
        assert "KeyError parsing build status" in caplog.text

    @staticmethod
    def test_build_details_returns_app_id_if_no_version(caplog):
        test_data = {"buildinfo": {
            "@app_id": "test_app_id",
            "build": {
                "analysis_unit": {
                    "@status": "test_status"
                }
            }
        }}
        result = BuildDetails.parse_build_details(test_data)
        assert result.app_id == "test_app_id"
        assert result.status == "test_status"
        assert not result.version
        assert "KeyError parsing build status" in caplog.text

    @staticmethod
    def test_build_details_no_previous_build():
        test_data = {}
        app_id = "1234"
        result = BuildDetails.parse_build_details(test_data, app_id=app_id)
        assert result.app_id == "1234"
        assert not result.status
