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
from security_scan_invoker.iface_build_details_fetcher import IBuildDetailsFetcher
from security_scan_invoker.build_details import BuildDetails
from security_scan_invoker.iface_veracode_api import IVeracodeAPI
from .parser import ScannerArgs


class VeracodeScannerCheckerException(Exception):
    """Internal exception in order to check build statuses and exit codes.

    :param Exception: Base exception to subtype from
    :type Exception: Exception
    """

    def __init__(self, message_path, exit_code: int = 0):
        super().__init__()
        self.message = f"Failed when running {message_path}"
        self.exit_code = exit_code


class VeracodeScannerApp:

    def __init__(
            self,
            args: ScannerArgs,
            build_details_fetcher: IBuildDetailsFetcher,
            veracode_api: IVeracodeAPI):
        logger = logging.getLogger(__name__)
        self.args: ScannerArgs = args
        self.veracode_api: IVeracodeAPI = veracode_api

        self.build_details_fetcher: IBuildDetailsFetcher = build_details_fetcher
        self.build_details: BuildDetails = \
            self.build_details_fetcher.get_build_details(args.app_name)

        if not self.build_details.status:
            logger.warning("Unable to get the previous scan status. Proceeding with a"
                           "scan for version %s", args.version)

    def run(self) -> int:
        """Runs the Veracode Scanner app. Will check the status of any previous scan and the state,
        and will launch a new scan if needed.

        :return: The exit code for the run. 0 if successful, 1 if an error, and 101 if no new scan
        is needed.
        :raises SystemExit: If there was an error and is unable to start a scan
        :rtype: int
        """

        logger = logging.getLogger(__name__)

        exit_code = self._run_pre_scan_checks()

        if exit_code > 0:
            if exit_code == 101:
                logger.info("A new scan is not needed. "
                            "Marking the current build successful.")
            else:
                logger.error("Scan failed to upload. Marking build step failed."
                             "See stack trace for ERROR and then visit: "
                             "https://github.com/JohnDeere/security-scan-invoker#"
                             "faq-and-common-errors")
        else:
            self._run_veracode_scan()

        return exit_code

    def _run_veracode_scan(self):
        """Uploads and starts a new Veracode scan.

        :raises SystemExit: If there was an error and is unable to start a scan
        """

        try:
            VeracodeScannerApp._submission_checker(
                self.veracode_api.upload_file(
                    self.build_details.app_id, self.args.filepath), "upload_file")

            VeracodeScannerApp._submission_checker(
                self.veracode_api.begin_prescan(
                    self.build_details.app_id), "begin_prescan")

            VeracodeScannerApp._submission_checker(
                self.veracode_api.get_prescan_results(
                    self.build_details.app_id), "get_prescan_results")

            VeracodeScannerApp._submission_checker(
                self.veracode_api.begin_scan(
                    self.build_details.app_id,
                    self.args.select_previous_modules),
                "begin_scan"
            )

        except VeracodeScannerCheckerException as err_status:
            raise SystemExit("Unable to submit or start Veracode scan. View logs for details. "
                             f"{err_status.message}") from err_status

    @staticmethod
    def _submission_checker(result: bool, message_path: str):
        """Checks the submission result, and will throw a VeracodeScannerCheckerException if there
        is.

        :param result: Result of a step in running a Veracode scan
        :type result: bool
        :raises VeracodeScannerCheckerException: Ex to raise if there is an error
        """

        if not result:
            raise VeracodeScannerCheckerException(message_path)

    def _run_pre_scan_checks(self) -> int:
        """Checks on the status of previous scans.

        :return: The exit code of the pre-scan checks
        :rtype: int
        """

        logger = logging.getLogger(__name__)

        if self.build_details.status:
            try:
                VeracodeScannerApp._status_checker(
                    VeracodeScannerApp._if_status_in_progress_status(
                        self.build_details), "if_status_in_progress_status")

                VeracodeScannerApp._status_checker(
                    self._if_status_in_failed_status(self.build_details, self.args.version),
                    "if_status_in_failed_status")

                VeracodeScannerApp._status_checker(
                    VeracodeScannerApp._if_status_in_successful_status_with_same_version(
                        self.build_details,
                        self.args.version),
                    "if_status_in_successful_status_with_same_version")

                VeracodeScannerApp._status_checker(
                    VeracodeScannerApp._if_status_in_undefined_status(self.build_details),
                    "if_status_in_undefined_status")

            except VeracodeScannerCheckerException as status:
                logger.error(f"Error with pre-scan checks. {status.message}")
                return status.exit_code

            logger.info("Proceeding with a scan for version %s", self.args.version)

        return 0

    @staticmethod
    def _status_checker(exit_code: int, message_path: str):
        """Checks the status of the exit_code given, and will raise a
        VeracodeScannerCheckerException if it is non 0.

        :param exit_code: Exit code to check for errors
        :type exit_code: int
        :raises VeracodeScannerCheckerException: Ex to raise if there is an error
        """

        if exit_code > 0:
            raise VeracodeScannerCheckerException(message_path, exit_code)

    @staticmethod
    def _if_status_in_progress_status(build_details: BuildDetails) -> int:
        """Checks if the build status is in progress.

        :param build_details: The build details to check the status on
        :type build_details: BuildDetails
        :return: 0 if there is not a build in progress, 101 if it is
        :rtype: int
        """

        logger = logging.getLogger(__name__)
        if build_details.status.lower() in BuildDetails.in_progress_build_status_list:
            logger.warning("Previous scan status: %s", build_details.status)
            return 101

        return 0

    def _if_status_in_failed_status(self, build_details: BuildDetails,
                                    version: str) -> int:
        """Checks if the build is in a failed state.

        :param build_details: The build details to check
        :type build_details: BuildDetails
        :param version: The version to check
        :type version: str
        :return: Exit code 0 if alright, 101 if there is an error
        :rtype: int
        """

        if build_details.status.lower() in BuildDetails.failed_build_status_list:
            return self._handle_previous_build_in_failed_status(build_details, version)
        return 0

    @staticmethod
    def _if_status_in_successful_status_with_same_version(
            build_details: BuildDetails, version: str) -> int:
        """Checks if the build is successful and the version matches.

        :param build_details: The build details to check
        :type build_details: BuildDetails
        :param version: The version to check
        :type version: str
        :return: Exit code 101 if trying to scan a version which has already succeeded, 0 otherwise
        :rtype: int
        """

        logger = logging.getLogger(__name__)
        if (
                build_details.status.lower() in BuildDetails.successful_build_status_list
                and build_details.version == version
        ):
            logger.warning("You are trying to scan version %s, which already succeeded",
                           build_details.version)
            return 101

        return 0

    @staticmethod
    def _if_status_in_undefined_status(build_details: BuildDetails) -> int:
        """Checks if the build details status is in an undefined state.

        :param build_details: The build details to check
        :type build_details: BuildDetails
        :return: 101 if undefined, 0 otherwise
        :rtype: int
        """
        if (
                build_details.status.lower() not in BuildDetails.successful_build_status_list
                and build_details.status.lower() not in BuildDetails.failed_build_status_list
                and build_details.status.lower() not in BuildDetails.in_progress_build_status_list
        ):
            logger = logging.getLogger(__name__)
            logger.error(
                f"The following build status is not handled: {build_details.status}")
            return 1

        return 0

    def _handle_previous_build_in_failed_status(
            self, build_details: BuildDetails, version: str) -> int:
        """Handles the build if there is a failed status.

        :param build_details: The build details to handle
        :type build_details: BuildDetails
        :param version: The new version to use
        :type version: str
        :return: Exit code if able to delete the previous scan, 101 if it is the same.
        :rtype: int
        """

        logger = logging.getLogger(__name__)
        if build_details.version == version:
            logger.error(f"ERROR: You are trying to scan version {build_details.version}"
                         ", which is the same version as the previous scan, and it is"
                         f" in bad state: {build_details.status}")
            return 1

        if build_details.status.lower() == "pre-scan failed":
            logger.warning(
                f"The previous scan for version {build_details.version} failed during the pre-scan."
                " If you see \"pre-scan failed\" multiple times, you should investigate",
            )
        else:
            logger.warning("The previous scan for version %s is in a bad state: %s"
                           ". Deleting it.", build_details.version, build_details.status)
        self.build_details_fetcher.delete_build_info(build_details.app_id)
        logger.info("Successfully requested deletion of the previous scan. Proceeding with a "
                    "scan for version %s", version)
        return 0
