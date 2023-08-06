# Copyright 2021-2023 Deere & Company.

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
from requests import HTTPError

from security_scan_invoker.build_details import BuildDetails
from security_scan_invoker.iface_build_details_fetcher import IBuildDetailsFetcher


class BuildDetailsFetcher(IBuildDetailsFetcher):
    def get_build_details(self, app_name) -> BuildDetails:
        apps = self.veracode_api.get_app_list()
        app_id = self.find_app_id(apps, app_name)
        response = self.veracode_api.get_build_info(app_id)
        return BuildDetails.parse_build_details(response, app_id)

    @staticmethod
    def find_app_id(apps, app_name):
        for app in apps:
            if app["@app_name"] == app_name:
                return app["@app_id"]
        raise SystemExit(
            "ERROR: Can't find app called "
            + app_name
            + " in any of the "
            + str(len(apps))
            + " apps associated with your ID and Key."
        )

    def delete_build_info(self, app_id):
        """Deletes the latest build of the given app_id.
        Will throw a SystemException if there was an issue with the request, otherwise
        will return a string of the response."""
        logger = logging.getLogger(__name__)
        try:
            content: dict = self.veracode_api.delete_build_info(app_id)
        except HTTPError as err_http:
            raise SystemExit(
                "ERROR: We found an issue in deleting the previous scan, which is in bad state."
                f" Error: {err_http}"
            ) from Exception
        except (TypeError, ValueError) as err_typeval:
            result_string = f"Unable to parse delete_build_info content. Error: {err_typeval}"
        else:
            # If the req was successful, then check the response
            if "deletebuildresult" in content:
                if "result" in content["deletebuildresult"]:
                    result_string = "Delete completed successfully with status: " \
                        f"{content['deletebuildresult']['result']}"
                else:
                    result_string = "Delete call completed but did not list a result: " \
                        f"{content['deletebuildresult']}"
            elif "error" in content:
                result_string = f"Error in running Delete: {content['error']}"
            else:
                result_string = "Delete call completed but did not list a valid result: " \
                    f"{content}"

        logger.info(result_string)
        return result_string
