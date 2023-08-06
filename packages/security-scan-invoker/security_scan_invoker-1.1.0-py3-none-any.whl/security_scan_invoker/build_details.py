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

import logging


class BuildDetails:
    in_progress_build_status_list: list[str] = [
        "scan in process",
        "pre-scan submitted",
        "pre-scan success",
        "submitted to engine",
        "pending internal review"
    ]
    failed_build_status_list: list[str] = [
        "incomplete",
        "scan canceled",
        "no modules defined",
        "pre-scan canceled",
        "pre-scan failed",
        "pending internal review",
        "not submitted to engine",
    ]
    successful_build_status_list: list[str] = ["results ready"]
    prescan_in_progress: str = "prescan results not available for application"

    def __init__(self, status: str, version: str, app_id: str):
        self.status: str = status
        self.version: str = version
        self.app_id: str = app_id

    @staticmethod
    def parse_build_details(build_info_response: dict, app_id: str = None) -> "BuildDetails":
        if "buildinfo" not in build_info_response:
            return BuildDetails(status=None, version=None, app_id=app_id)

        if not app_id:
            app_id = build_info_response["buildinfo"]["@app_id"]

        status = ""
        version = ""

        try:
            status = build_info_response["buildinfo"]["build"]["analysis_unit"]["@status"]
            version = build_info_response["buildinfo"]["build"]["@version"]
        except KeyError as err_key:
            logger = logging.getLogger(__name__)
            logger.warning(f"KeyError parsing build status. Err: {err_key}, "
                           f"resp:{build_info_response}")

        return BuildDetails(status, version, app_id)

    @staticmethod
    def check_build_status(status) -> bool:
        status_lower = status.lower()
        if status_lower in BuildDetails.successful_build_status_list or \
                status_lower in BuildDetails.in_progress_build_status_list:
            return True
        return False
