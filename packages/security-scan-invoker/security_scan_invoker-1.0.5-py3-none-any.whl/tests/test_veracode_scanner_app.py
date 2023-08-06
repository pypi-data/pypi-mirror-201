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

import mock
import pytest
from security_scan_invoker.parser import ScannerArgs

from security_scan_invoker.veracode_scanner_app import VeracodeScannerApp
from security_scan_invoker.build_details import BuildDetails
from .fake_build_details_fetcher import FakeBuildDetailsFetcher
from .fake_veracode_api import FakeVeracodeAPI


@pytest.fixture(name="patched_build_submission")
def mock_build_submission():
    with mock.patch.object(VeracodeScannerApp, "_run_veracode_scan") as mocked_run_veracode_scan:
        yield mocked_run_veracode_scan


@pytest.fixture(name="patched_pre_scan_checks")
def mock_pre_scan_checks():
    with mock.patch.object(VeracodeScannerApp, "_run_pre_scan_checks") as \
            mocked_run_pre_scan_checks:
        mocked_run_pre_scan_checks.return_value = 0
        yield mocked_run_pre_scan_checks


@pytest.fixture(name="patched_build_details_fetcher")
def mock_build_details_fetcher():
    yield FakeBuildDetailsFetcher(BuildDetails("", "", ""))


@pytest.fixture(name="fake_veracode_api")
def mock_fake_veracode_api():
    yield FakeVeracodeAPI()

# pylint: disable=too-many-public-methods


class TestVeracodeScannerApp:
    @staticmethod
    def check_no_new_scan_needed_text(text):
        assert "We do not need to start a new scan. " \
            "We are marking the current build successful." in text

    @staticmethod
    def get_scanning_args(
            appname: str,
            version: str) -> ScannerArgs:
        return ScannerArgs({
            "appname": appname,
            "version": version,
            "vkey": "test_key",
            "vid": "test_id",
            "filepath": "test_filepath",
            "select_previous_modules": False
        })

    class TestPreScanChecks:
        @staticmethod
        def test_job_gets_build_details_for_app(patched_build_submission, fake_veracode_api):
            build_details = BuildDetails("Results Ready", "GIT HASH", "")
            build_status_fetcher = FakeBuildDetailsFetcher(build_details)
            args = TestVeracodeScannerApp.get_scanning_args(
                "my_app", "GIT HASH 2")
            VeracodeScannerApp(args, build_status_fetcher, fake_veracode_api).run()

            patched_build_submission.assert_called_once()
            assert build_status_fetcher.app_name_received == "my_app"

        @staticmethod
        def test_job_run_handles_exception_when_build_details_not_found(
                patched_build_submission, fake_veracode_api, caplog):
            build_details = BuildDetails("", "", "")
            build_status_fetcher = FakeBuildDetailsFetcher(build_details)
            args = TestVeracodeScannerApp.get_scanning_args(
                "", "GIT HASH 2")
            VeracodeScannerApp(args, build_status_fetcher, fake_veracode_api).run()

            assert "GIT HASH 2" in caplog.text
            assert "Unable to get the previous scan status." in caplog.text
            patched_build_submission.assert_called_once()

        @staticmethod
        def test_job_run_exits_gracefully_when_build_status_is_scan_in_process(
                fake_veracode_api, caplog):
            build_details = BuildDetails("Scan In Process", "", "")
            build_status_fetcher = FakeBuildDetailsFetcher(build_details)
            args = TestVeracodeScannerApp.get_scanning_args("", "GIT HASH 2")
            exit_code = VeracodeScannerApp(args, build_status_fetcher, fake_veracode_api).run()

            assert exit_code == 101
            assert "Scan In Process" in caplog.text

        @staticmethod
        def test_job_run_exits_gracefully_when_build_status_is_pre_scan_submitted(
                fake_veracode_api, caplog):
            build_details = BuildDetails("Pre-Scan Submitted", "", "")
            build_status_fetcher = FakeBuildDetailsFetcher(build_details)
            args = TestVeracodeScannerApp.get_scanning_args("", "",)
            exit_code = VeracodeScannerApp(args, build_status_fetcher, fake_veracode_api).run()

            assert exit_code == 101
            assert "Pre-Scan Submitted" in caplog.text

        @staticmethod
        def test_job_run_exits_gracefully_when_build_status_is_pre_scan_success(
                fake_veracode_api, caplog):
            build_details = BuildDetails("Pre-Scan Success", "", "")
            build_status_fetcher = FakeBuildDetailsFetcher(build_details)
            args = TestVeracodeScannerApp.get_scanning_args("", "")
            exit_code = VeracodeScannerApp(args, build_status_fetcher, fake_veracode_api).run()

            assert exit_code == 101
            assert "Pre-Scan Success" in caplog.text

        @staticmethod
        def test_job_run_exits_with_error_when_build_status_not_defined(
                fake_veracode_api, caplog):
            build_details = BuildDetails("Pre-scan Failed", "", "")
            build_status_fetcher = FakeBuildDetailsFetcher(build_details)
            args = TestVeracodeScannerApp.get_scanning_args("", "")
            exit_code = VeracodeScannerApp(args, build_status_fetcher, fake_veracode_api).run()

            assert exit_code == 1
            assert "ERROR:" in caplog.text
            assert "Pre-scan Failed" in caplog.text

        @staticmethod
        def test_job_run_exits_gracefully_when_version_is_same_and_build_status_is_results_ready(
                fake_veracode_api, caplog):
            build_details = BuildDetails("Results Ready", "GIT HASH", "")
            build_status_fetcher = FakeBuildDetailsFetcher(build_details)
            args = TestVeracodeScannerApp.get_scanning_args("", "GIT HASH")
            exit_code = VeracodeScannerApp(args, build_status_fetcher, fake_veracode_api).run()

            assert exit_code == 101
            assert "GIT HASH" in caplog.text

        @staticmethod
        def test_job_run_proceeds_when_version_is_the_same_and_allow_rescan_is_false(
                fake_veracode_api, caplog):
            build_details = BuildDetails("Results Ready", "GIT HASH", "")
            build_status_fetcher = FakeBuildDetailsFetcher(build_details)
            args = TestVeracodeScannerApp.get_scanning_args("", "GIT HASH")
            exit_code = VeracodeScannerApp(args, build_status_fetcher, fake_veracode_api).run()

            assert exit_code == 101
            assert "GIT HASH" in caplog.text

        @staticmethod
        def test_job_run_proceeds_when_version_is_the_same_and_allow_rescan_is_none(
                fake_veracode_api, caplog):
            build_details = BuildDetails("Results Ready", "GIT HASH", "")
            build_status_fetcher = FakeBuildDetailsFetcher(build_details)
            args = TestVeracodeScannerApp.get_scanning_args("", "GIT HASH")
            exit_code = VeracodeScannerApp(args, build_status_fetcher, fake_veracode_api).run()

            assert exit_code == 101
            assert "GIT HASH" in caplog.text

        @staticmethod
        def test_job_run_proceeds_with_scan_when_build_status_is_results_ready(
                patched_build_submission, fake_veracode_api, caplog):
            build_details = BuildDetails("Results Ready", "GIT HASH", "")
            build_status_fetcher = FakeBuildDetailsFetcher(build_details)
            args = TestVeracodeScannerApp.get_scanning_args(
                "",
                "GIT HASH 2"
            )

            exit_code = VeracodeScannerApp(args, build_status_fetcher, fake_veracode_api).run()

            assert exit_code == 0
            assert "GIT HASH 2" in caplog.text
            patched_build_submission.assert_called_once()

        @staticmethod
        def test_job_run_exits_with_error_when_version_is_the_same_and_build_status_is_incomplete(
                fake_veracode_api, caplog):
            build_details = BuildDetails("Incomplete", "GIT HASH", "")
            build_status_fetcher = FakeBuildDetailsFetcher(build_details)
            args = TestVeracodeScannerApp.get_scanning_args("", "GIT HASH")
            exit_code = VeracodeScannerApp(args, build_status_fetcher, fake_veracode_api).run()

            assert exit_code == 1
            assert "ERROR:" in caplog.text
            assert "GIT HASH" in caplog.text
            assert "Incomplete" in caplog.text

        @staticmethod
        def test_job_run_exits_gracefully_when_build_status_is_not_submitted_to_engine(
                fake_veracode_api, caplog):
            build_details = BuildDetails("Not Submitted to Engine", "", "")
            build_status_fetcher = FakeBuildDetailsFetcher(build_details)
            args = TestVeracodeScannerApp.get_scanning_args("", "")
            exit_code = VeracodeScannerApp(args, build_status_fetcher, fake_veracode_api).run()

            assert exit_code == 1
            assert "Not Submitted to Engine" in caplog.text

        @staticmethod
        def test_job_run_exits_with_error_when_version_is_same_and_build_status_is_scan_cancelled(
                fake_veracode_api, caplog):
            build_details = BuildDetails("Scan Canceled", "GIT HASH", "")
            build_status_fetcher = FakeBuildDetailsFetcher(build_details)
            args = TestVeracodeScannerApp.get_scanning_args("", "GIT HASH")
            exit_code = VeracodeScannerApp(args, build_status_fetcher, fake_veracode_api).run()

            assert exit_code == 1
            assert "ERROR:" in caplog.text
            assert "GIT HASH" in caplog.text
            assert "Scan Canceled" in caplog.text

        @staticmethod
        def test_job_run_exits_gracefully_when_build_status_is_pending_internal_review(
                fake_veracode_api, caplog):
            build_details = BuildDetails("Pending Internal Review", "", "")
            build_status_fetcher = FakeBuildDetailsFetcher(build_details)
            args = TestVeracodeScannerApp.get_scanning_args("", "GIT HASH 2")
            exit_code = VeracodeScannerApp(args, build_status_fetcher, fake_veracode_api).run()

            assert exit_code == 101
            assert "Pending Internal Review" in caplog.text

        @staticmethod
        def test_job_run_exits_with_error_when_vers_matches_and_build_status_is_no_modules_defined(
                fake_veracode_api, caplog):
            build_details = BuildDetails("No Modules Defined", "GIT HASH", "")
            build_status_fetcher = FakeBuildDetailsFetcher(build_details)
            args = TestVeracodeScannerApp.get_scanning_args("", "GIT HASH")
            exit_code = VeracodeScannerApp(args, build_status_fetcher, fake_veracode_api).run()

            assert exit_code == 1
            assert "ERROR:" in caplog.text
            assert "GIT HASH" in caplog.text
            assert "No Modules Defined" in caplog.text

        @staticmethod
        def test_job_run_exits_with_error_when_vers_matches_and_build_status_is_pre_scan_cancelled(
                fake_veracode_api, caplog):
            build_details = BuildDetails("Pre-scan Canceled", "GIT HASH", "")
            build_status_fetcher = FakeBuildDetailsFetcher(build_details)
            args = TestVeracodeScannerApp.get_scanning_args("", "GIT HASH")
            exit_code = VeracodeScannerApp(args, build_status_fetcher, fake_veracode_api).run()

            assert exit_code == 1
            assert "ERROR:" in caplog.text
            assert "GIT HASH" in caplog.text
            assert "Pre-scan Canceled" in caplog.text

        @staticmethod
        def test_job_deletes_previous_scan_when_build_status_is_incomplete(
                patched_build_submission, fake_veracode_api, caplog):
            build_details = BuildDetails("Incomplete", "GIT HASH", "5067")
            build_status_fetcher = FakeBuildDetailsFetcher(build_details)
            args = TestVeracodeScannerApp.get_scanning_args("", "GIT HASH 2")
            exit_code = VeracodeScannerApp(args, build_status_fetcher, fake_veracode_api).run()

            assert exit_code == 0
            assert build_status_fetcher.app_id_deleted == "5067"
            assert "The previous scan for version GIT HASH" in caplog.text
            assert "Incomplete" in caplog.text
            assert "Proceeding with a scan for version GIT HASH 2" in caplog.text
            patched_build_submission.assert_called_once()

        @staticmethod
        def test_job_deletes_previous_scan_when_build_status_is_scan_cancelled(
                patched_build_submission, fake_veracode_api, caplog):
            build_details = BuildDetails("Scan Canceled", "GIT HASH", "5067")
            build_status_fetcher = FakeBuildDetailsFetcher(build_details)
            args = TestVeracodeScannerApp.get_scanning_args("", "GIT HASH 2")
            exit_code = VeracodeScannerApp(args, build_status_fetcher, fake_veracode_api).run()

            assert exit_code == 0
            assert build_status_fetcher.app_id_deleted == "5067"
            assert "The previous scan for version GIT HASH" in caplog.text
            assert "Scan Canceled" in caplog.text
            assert "Proceeding with a scan for version GIT HASH 2" in caplog.text
            patched_build_submission.assert_called_once()

        @staticmethod
        def test_job_deletes_previous_scan_when_build_status_is_no_modules_defined(
                patched_build_submission, fake_veracode_api, caplog):
            build_details = BuildDetails("No Modules Defined", "GIT HASH", "5067")
            build_status_fetcher = FakeBuildDetailsFetcher(build_details)
            args = TestVeracodeScannerApp.get_scanning_args("", "GIT HASH 2")
            exit_code = VeracodeScannerApp(args, build_status_fetcher, fake_veracode_api).run()

            assert exit_code == 0
            assert build_status_fetcher.app_id_deleted == "5067"
            assert "The previous scan for version GIT HASH" in caplog.text
            assert "No Modules Defined" in caplog.text
            assert "Proceeding with a scan for version GIT HASH 2" in caplog.text
            patched_build_submission.assert_called_once()

        @staticmethod
        def test_job_deletes_previous_scan_when_build_status_is_pre_scan_cancelled(
                patched_build_submission, fake_veracode_api, caplog):
            build_details = BuildDetails("Pre-scan Canceled", "GIT HASH", "5067")
            build_status_fetcher = FakeBuildDetailsFetcher(build_details)
            args = TestVeracodeScannerApp.get_scanning_args("", "GIT HASH 2")
            exit_code = VeracodeScannerApp(args, build_status_fetcher, fake_veracode_api).run()

            assert exit_code == 0
            assert build_status_fetcher.app_id_deleted == "5067"
            assert "The previous scan for version GIT HASH" in caplog.text
            assert "Pre-scan Canceled" in caplog.text
            assert "Proceeding with a scan for version GIT HASH 2" in caplog.text
            patched_build_submission.assert_called_once()

        @staticmethod
        def test_job_deletes_previous_scan_when_build_status_is_pre_scan_failed(
                patched_build_submission, fake_veracode_api, caplog):
            build_details = BuildDetails("Pre-scan Failed", "GIT HASH", "5067")
            build_status_fetcher = FakeBuildDetailsFetcher(build_details)
            args = TestVeracodeScannerApp.get_scanning_args("", "GIT HASH 2")
            exit_code = VeracodeScannerApp(args, build_status_fetcher, fake_veracode_api).run()

            assert exit_code == 0
            assert build_status_fetcher.app_id_deleted == "5067"
            assert "The previous scan for version GIT HASH" in caplog.text
            assert "If you see \"pre-scan failed\" multiple times" in caplog.text
            assert "Proceeding with a scan for version GIT HASH 2" in caplog.text
            patched_build_submission.assert_called_once()

        @staticmethod
        def test_job_fails_when_build_status_is_undefined(
                fake_veracode_api, caplog):
            build_details = BuildDetails("A NOT REAL STATUS", "GIT HASH", "5067")
            build_status_fetcher = FakeBuildDetailsFetcher(build_details)
            args = TestVeracodeScannerApp.get_scanning_args("", "GIT HASH 2")
            exit_code = VeracodeScannerApp(args, build_status_fetcher, fake_veracode_api).run()
            assert exit_code == 1
            assert "The following build status is not handled" in caplog.text
            assert "A NOT REAL STATUS" in caplog.text

        @staticmethod
        def test_job_run_exits_gracefully_when_build_status_is_submitted_to_engine(
                fake_veracode_api, caplog):
            build_details = BuildDetails("Submitted to Engine", "", "")
            build_status_fetcher = FakeBuildDetailsFetcher(build_details)
            args = TestVeracodeScannerApp.get_scanning_args("", "")
            exit_code = VeracodeScannerApp(args, build_status_fetcher, fake_veracode_api).run()

            assert exit_code == 101
            assert "Submitted to Engine" in caplog.text

    class TestRunVeracodeScan:
        @staticmethod
        def test_upload_file_succeeds(
                patched_pre_scan_checks,
                patched_build_details_fetcher,
                fake_veracode_api):
            fake_veracode_api.upload_file_result = True
            args = TestVeracodeScannerApp.get_scanning_args("", "")
            assert VeracodeScannerApp(
                args,
                patched_build_details_fetcher,
                fake_veracode_api).run() == 0
            patched_pre_scan_checks.assert_called_once()

        @staticmethod
        def test_upload_file_fails(
                patched_pre_scan_checks,
                patched_build_details_fetcher,
                fake_veracode_api):
            with pytest.raises(SystemExit):
                fake_veracode_api.upload_file_result = False
                args = TestVeracodeScannerApp.get_scanning_args("", "")
                VeracodeScannerApp(args, patched_build_details_fetcher, fake_veracode_api).run()
            patched_pre_scan_checks.assert_called_once()

        @staticmethod
        def test_begin_prescan_succeeds(
                patched_pre_scan_checks,
                patched_build_details_fetcher,
                fake_veracode_api):
            fake_veracode_api.begin_prescan_result = True
            args = TestVeracodeScannerApp.get_scanning_args("", "")
            assert VeracodeScannerApp(
                args,
                patched_build_details_fetcher,
                fake_veracode_api).run() == 0
            patched_pre_scan_checks.assert_called_once()

        @staticmethod
        def test_begin_prescan_fails(
                patched_pre_scan_checks,
                patched_build_details_fetcher,
                fake_veracode_api):
            with pytest.raises(SystemExit):
                fake_veracode_api.begin_prescan_result = False
                args = TestVeracodeScannerApp.get_scanning_args("", "")
                VeracodeScannerApp(args, patched_build_details_fetcher, fake_veracode_api).run()
            patched_pre_scan_checks.assert_called_once()

        @staticmethod
        def test_get_prescan_results_succeeds(
                patched_pre_scan_checks,
                patched_build_details_fetcher,
                fake_veracode_api):
            fake_veracode_api.get_prescan_result = True
            args = TestVeracodeScannerApp.get_scanning_args("", "")
            assert VeracodeScannerApp(
                args,
                patched_build_details_fetcher,
                fake_veracode_api).run() == 0
            patched_pre_scan_checks.assert_called_once()

        @staticmethod
        def test_get_prescan_results_fails(
                patched_pre_scan_checks,
                patched_build_details_fetcher,
                fake_veracode_api):
            with pytest.raises(SystemExit):
                fake_veracode_api.get_prescan_result = False
                args = TestVeracodeScannerApp.get_scanning_args("", "")
                VeracodeScannerApp(args, patched_build_details_fetcher, fake_veracode_api).run()
            patched_pre_scan_checks.assert_called_once()

        @staticmethod
        def test_begin_scan_succeeds(
                patched_pre_scan_checks,
                patched_build_details_fetcher,
                fake_veracode_api):
            fake_veracode_api.begin_scan_result = True
            args = TestVeracodeScannerApp.get_scanning_args("", "")
            assert VeracodeScannerApp(
                args,
                patched_build_details_fetcher,
                fake_veracode_api).run() == 0
            patched_pre_scan_checks.assert_called_once()

        @staticmethod
        def test_begin_scan_fails(
                patched_pre_scan_checks,
                patched_build_details_fetcher,
                fake_veracode_api):
            with pytest.raises(SystemExit):
                fake_veracode_api.begin_scan_result = False
                args = TestVeracodeScannerApp.get_scanning_args("", "")
                VeracodeScannerApp(args, patched_build_details_fetcher, fake_veracode_api).run()
            patched_pre_scan_checks.assert_called_once()
