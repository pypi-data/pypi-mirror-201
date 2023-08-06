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

import logging


# pylint: disable=too-many-instance-attributes
class ScannerArgs:
    """Class to hold parameters defined for the Veracode Scanner process.
    """

    def __init__(self, args: dict):
        """Creates a ScannerArgs class.

        :param args: The parameters to define for the scan.
            Required arguments:
                appname: The name of the Veracode application to be scanned
                version: The new build version for the scan
                vid: The Veracode API ID
                vkey: The Veracode API key
                filepath: The path of the package to be scanned

            Optional:
                select_previous_modules: If the scan should select previous modules to use
        :type args: dict
        :raises AttributeError: Raises an if there is a parameter missing
        """

        try:
            self.app_name: str = args["appname"]
            self.version: str = args["version"]
            self.vkey: str = args["vkey"]
            self.vid: str = args["vid"]
            self.filepath: str = args["filepath"]
            self.select_previous_modules: bool = args["select_previous_modules"]
        except KeyError as err_key:
            logger = logging.getLogger(__name__)
            logger.error("Unable to create ScannerArgs object. Missing parameter.")
            raise err_key
