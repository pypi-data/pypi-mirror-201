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

from security_scan_invoker.iface_build_details_fetcher import IBuildDetailsFetcher


class FakeBuildDetailsFetcher(IBuildDetailsFetcher):
    def __init__(self, build_details_to_return):
        super().__init__(None)  # type: ignore
        self.app_name_received = ""
        self.build_details_to_return = build_details_to_return
        self.app_id_deleted = 0

    def get_build_details(self, app_name):
        self.app_name_received = app_name
        return self.build_details_to_return

    def delete_build_info(self, app_id):
        self.app_id_deleted = app_id
