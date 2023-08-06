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
import time
from requests import HTTPError
import xmltodict
import requests
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC
from security_scan_invoker.build_details import BuildDetails


from .iface_veracode_api import IVeracodeAPI


class VeracodeAPIWrapper(IVeracodeAPI):

    base_url = "https://analysiscenter.veracode.com/api/"
    base_v3 = f"{base_url}3.0/"
    base_v5 = f"{base_url}5.0/"

    def __init__(self, api_key_id: str, api_key_secret: str):
        self.api_key_id = api_key_id
        self.api_key_secret = api_key_secret

    def get_app_list(self):
        url = self.base_v3 + "getapplist.do"
        res = requests.get(
            url,
            params={},
            auth=RequestsAuthPluginVeracodeHMAC(
                api_key_id=self.api_key_id, api_key_secret=self.api_key_secret
            ),
            timeout=60
        )
        res.raise_for_status()
        content = xmltodict.parse(res.content, force_list={"app"})
        return content["applist"]["app"]

    def get_build_info(self, app_id: str) -> dict:
        url = self.base_v3 + "getbuildinfo.do"
        params = {"app_id": app_id}
        res = requests.get(
            url,
            params=params,
            auth=RequestsAuthPluginVeracodeHMAC(
                api_key_id=self.api_key_id, api_key_secret=self.api_key_secret
            ),
            timeout=60
        )
        res.raise_for_status()
        return xmltodict.parse(res.content)

    def delete_build_info(self, app_id: str) -> dict:
        url = self.base_v3 + "deletebuild.do"
        params = {"app_id": app_id}
        res = requests.get(
            url,
            params=params,
            auth=RequestsAuthPluginVeracodeHMAC(
                api_key_id=self.api_key_id, api_key_secret=self.api_key_secret
            ),
            timeout=60
        )
        res.raise_for_status()
        return xmltodict.parse(res.content)

    def upload_file(self, app_id: str, filepath: str) -> bool:
        """Uploads a file for scanning.

        :param app_id: The ID of the app to scan
        :type app_id: str
        :param filepath: The filepath of the file(s) to submit for scanning
        :type filepath: str
        :raises err: HTTPError if there was an error in the request.
        :return: True if the files were submitted successfully, False otherwise
        :rtype: bool
        """

        logger = logging.getLogger(__name__)
        # Uses the uploadlargefile.do endpoint since that just has a longer timeout
        # than the normal endpoint
        url = self.base_v5 + "uploadlargefile.do"
        try:
            with open(filepath, "rb") as file:
                res = requests.post(
                    url,
                    headers={
                        "Content-Type": "binary/octet-stream"},
                    params={
                        "app_id": app_id,
                        "filename": filepath},
                    data=file,
                    auth=RequestsAuthPluginVeracodeHMAC(
                        api_key_id=self.api_key_id,
                        api_key_secret=self.api_key_secret),
                    timeout=60
                )

                res.raise_for_status()
        except HTTPError as err:
            logger.error(f'HTTP Error occurred: {err}')
            raise err

        parsed = xmltodict.parse(res.text)
        if "error" in parsed and parsed["error"]:
            logger.error(f"Error with file upload -- {parsed['error']}")
            return False

        file = parsed["filelist"]["file"]
        if file["@file_status"] != "Uploaded":
            logger.error(f"Unsuccessful upload of file {file}")
            return False

        return True

    def begin_prescan(self, app_id: str, autoscan: bool = False) -> bool:
        """Begins the prescan after successfully uploading a file.

        :param app_id: The app id to start the prescan on
        :type app_id: str
        :param autoscan: If it should auto-scan, defaults to False
        :type autoscan: bool, optional
        :raises err: HTTPError if there was an error in the request.
        :return: True if the scan started successfully, False otherwise
        :rtype: bool
        """
        logger = logging.getLogger(__name__)
        url = self.base_v5 + "beginprescan.do"
        params = {"app_id": app_id, "auto_scan": autoscan}
        try:
            res = requests.get(
                url,
                params=params,
                auth=RequestsAuthPluginVeracodeHMAC(
                    api_key_id=self.api_key_id, api_key_secret=self.api_key_secret
                ),
                timeout=60
            )
            res.raise_for_status()
        except HTTPError as err:
            logger.error(f'HTTP Error occurred: {err}')
            raise err

        build_details = BuildDetails.parse_build_details(xmltodict.parse(res.text))
        return BuildDetails.check_build_status(build_details.status)

    def get_prescan_results(self, app_id: str) -> bool:
        """Gets the prescan results for the given app_id.
        Will retry up to 5 times to get the results of the pre-scan.

        :param app_id: The app id to start the prescan on
        :type app_id: str
        :raises err: HTTPError if there was an error in the request.
        :return: True if the pre-scan was successful, False otherwise
        :rtype: bool
        """

        logger = logging.getLogger(__name__)
        url = self.base_v5 + "getprescanresults.do"
        params = {"app_id": app_id}
        attempt: int = 0
        while attempt < 10:
            attempt += 1
            try:
                res = requests.get(
                    url,
                    params=params,
                    auth=RequestsAuthPluginVeracodeHMAC(
                        api_key_id=self.api_key_id, api_key_secret=self.api_key_secret
                    ),
                    timeout=60
                )
                res.raise_for_status()
            except HTTPError as err:
                logger.error(f'HTTP Error occurred: {err}')
                raise err

            parsed = xmltodict.parse(res.text)
            if "error" in parsed:
                if attempt >= 10:
                    logger.error(f"Unable to complete pre-scan. Error {parsed}")
                else:
                    time.sleep(30)
            else:
                if "prescanresults" in parsed:
                    return parsed["prescanresults"]["module"]["@status"].lower() == "ok"

        return False

    def begin_scan(self, app_id: str, select_previous_modules: bool) -> bool:
        """Begins the scan for the given app_id.

        :param app_id: The app id to start the prescan on
        :type app_id: str
        :param select_previous_modules: Whether to use the previous modules selection for scan
        :type select_previous_modules: bool
        :raises err: HTTPError if there was an error in the request.
        :return: True if the scan was started, False otherwise
        :rtype: bool
        """
        logger = logging.getLogger(__name__)
        url = self.base_v5 + "beginscan.do"
        modules_to_scan: str = "select_previous_modules" if select_previous_modules \
            else "scan_all_top_level_modules"
        params = {
            "app_id": app_id,
            modules_to_scan: True
        }
        try:
            res = requests.get(
                url,
                params=params,
                auth=RequestsAuthPluginVeracodeHMAC(
                    api_key_id=self.api_key_id, api_key_secret=self.api_key_secret
                ),
                timeout=60
            )
            res.raise_for_status()
        except HTTPError as err:
            logger.error(f'HTTP Error occurred: {err}')
            raise err

        parsed = xmltodict.parse(res.text)
        if "buildinfo" in parsed:
            return parsed["buildinfo"]["build"]["analysis_unit"]["@status"].lower() in \
                BuildDetails.in_progress_build_status_list

        return False
