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

import xmltodict
from requests import HTTPError
from security_scan_invoker.iface_veracode_api import IVeracodeAPI


# pylint: disable=too-many-instance-attributes


class FakeVeracodeAPI(IVeracodeAPI):
    def __init__(
        self, app_list=None, build_info_content=None,
        should_throw_error_delete_build=False,
        delete_build_content=None
    ):
        self.got_app_list = False
        self.app_id_received = "-1"
        if app_list:
            app_list_content = self.create_app_list_content(app_list)
            self.get_app_list_content = app_list_content

        self.get_app_list_status_code = 200
        self.get_build_info_content = build_info_content
        self.get_build_info_status_code = 200
        self.delete_build_info_status_code = 200
        self.should_throw_error_delete_build = should_throw_error_delete_build
        self.delete_build_content = delete_build_content

        self.begin_scan_result = True
        self.begin_prescan_result = True
        self.get_prescan_result = True
        self.upload_file_result = True

    # pylint: disable=protected-access
    def get_app_list(self):
        self.got_app_list = True
        if self.get_app_list_status_code > 200:
            raise HTTPError("status code over 200")
        return xmltodict.parse(self.get_app_list_content, force_list={"app"})["applist"]["app"]

    # pylint: disable=protected-access
    def get_build_info(self, app_id):
        self.app_id_received = app_id
        if self.get_build_info_status_code > 200:
            raise HTTPError("status code over 200")
        return xmltodict.parse(self.get_build_info_content)

    def delete_build_info(self, app_id):
        self.app_id_received = app_id
        if self.delete_build_info_status_code > 200 or self.should_throw_error_delete_build:
            raise HTTPError("status code over 200")
        return xmltodict.parse(self.create_delete_build_info_content(self.delete_build_content))

    def upload_file(self, app_id, filepath):
        return self.upload_file_result

    def begin_prescan(self, app_id):
        return self.begin_prescan_result

    def begin_scan(self, app_id, select_previous_modules):
        return self.begin_scan_result

    def get_prescan_results(self, app_id):
        return self.get_prescan_result

    @staticmethod
    def create_app_list_content(apps):
        app_list = "<applist>"
        for app in apps:
            app_list += (
                '<app app_id="'
                + app["app_id"]
                + '" app_name="'
                + app["app_name"]
                + '" policy_updated_date=""/>'
            )
        app_list += "</applist>"
        return app_list

    @staticmethod
    def create_delete_build_info_content(content_dict):
        """Takes in a dictionary of the content data and converts it to a mock xml format"""
        if content_dict is None:
            return None

        for key, val in content_dict.items():
            ret = f"<{key}>"
            if isinstance(val, dict):
                for ikey, ival in val.items():
                    ret = ret + f"<{ikey}>{ival}</{ikey}>"
            else:
                ret = ret + val
            ret = ret + f"</{key}>"
        return ret
