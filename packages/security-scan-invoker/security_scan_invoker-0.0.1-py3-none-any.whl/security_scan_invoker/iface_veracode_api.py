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

from abc import ABCMeta, abstractmethod


class IVeracodeAPI(metaclass=ABCMeta):
    @abstractmethod
    def get_app_list(self) -> dict:
        pass

    @abstractmethod
    def get_build_info(self, app_id: str) -> dict:
        pass

    @abstractmethod
    def delete_build_info(self, app_id: str) -> dict:
        pass

    @abstractmethod
    def upload_file(self, app_id: str, filepath: str) -> bool:
        pass

    @abstractmethod
    def begin_prescan(self, app_id: str) -> bool:
        pass

    @abstractmethod
    def get_prescan_results(self, app_id: str) -> bool:
        pass

    @abstractmethod
    def begin_scan(
            self,
            app_id: str,
            select_previous_modules: bool
    ) -> bool:
        pass
