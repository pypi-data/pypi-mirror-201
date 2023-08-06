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

from requests import HTTPError

FAKE_UPLOAD_FILE_SCAN_ALREADY_RUNNING = '<?xml version="1.0" encoding="UTF-8"?>\n\n<error>' \
    'Not in a state where file upload can occur.</error>\n'

FAKE_UPLOAD_FILE_SUCCESS = """<?xml version="1.0" encoding="UTF-8"?>\n\n<filelist xmlns:xsi="http
    &#x3a;&#x2f;&#x2f;www.w3.org&#x2f;2001&#x2f;XMLSchema-instance" xmlns="https&#x3a;&#x2f;
    &#x2f;analysiscenter.veracode.com&#x2f;schema&#x2f;2.0&#x2f;filelist" xsi:schemaLocation=
    "https&#x3a;&#x2f;&#x2f;analysiscenter.veracode.com&#x2f;schema&#x2f;2.0&#x2f;filelist https
    &#x3a;&#x2f;&#x2f;analysiscenter.veracode.com&#x2f;resource&#x2f;2.0&#x2f;filelist.xsd"
    filelist_version="1.1" account_id="testaccount_id" app_id="testapp_id" sandbox_id="
    test_sandbox_id" build_id="test_build_info_id"><file file_id="test_file_find_id" file_name=
    "test_files.zip" file_status="Uploaded"/>\n</filelist>\n"""

FAKE_UPLOAD_FILE_FAILED = """<?xml version="1.0" encoding="UTF-8"?>\n\n<filelist
    xmlns:xsi="http&#x3a;&#x2f;&#x2f;www.w3.org&#x2f;2001&#x2f;XMLSchema-instance"
    xmlns="https&#x3a;&#x2f;&#x2f;analysiscenter.veracode.com&#x2f;schema&#x2f;2.0&#x2f;filelist"
    xsi:schemaLocation="https&#x3a;&#x2f;&#x2f;analysiscenter.veracode.com&#x2f;schema&#x2f;
    2.0&#x2f;filelist https&#x3a;&#x2f;&#x2f;analysiscenter.veracode.com&#x2f;resource&#x2f;
    2.0&#x2f;filelist.xsd" filelist_version="1.1" account_id="testaccount_id" app_id="testapp_id"
    sandbox_id="test_sandbox_id" build_id="test_build_info_id"><file file_id="test_file_find_id"
    file_name="test_files.zip" file_status="Unsuccessful"/>\n</filelist>\n"""


FAKE_BEGIN_PRESCAN_SUCCESS = """<?xml version="1.0" encoding="UTF-8"?>\n\n<buildinfo
    xmlns:xsi="http&#x3a;&#x2f;&#x2f;www.w3.org&#x2f;2001&#x2f;XMLSchema-instance"
    xmlns="https&#x3a;&#x2f;&#x2f;analysiscenter.veracode.com&#x2f;schema&#x2f;4.0&#x2f;buildinfo"
    xsi:schemaLocation="https&#x3a;&#x2f;&#x2f;analysiscenter.veracode.com&#x2f;
    schema&#x2f;4.0&#x2f;buildinfo https&#x3a;&#x2f;&#x2f;analysiscenter.veracode.com&#x2f;
    resource&#x2f;4.0&#x2f;buildinfo.xsd" buildinfo_version="1.5"
    account_id="testaccount_id" app_id="testapp_id" build_id="test_build_id">
    <build version="6 Oct 2022 Static" build_id="test_build_id"
    submitter="Test User" platform="Not Specified" lifecycle_stage="Not Specified"
    results_ready="false" policy_name="Test Policy" policy_version="11"
    policy_compliance_status="Pass" policy_updated_date="2022-10-06T11&#x3a;28&#x3a;03-04&#x3a;00"
    rules_status="Pass" grace_period_expired="false" scan_overdue="false"
    legacy_scan_engine="false">\n<analysis_unit analysis_type="Static"
    status="Pre-Scan Submitted"/>\n   </build>\n</buildinfo>\n"""

FAKE_BEGIN_PRESCAN_FAILED = """<?xml version="1.0" encoding="UTF-8"?>\n\n
    <buildinfo xmlns:xsi="http&#x3a;&#x2f;&#x2f;www.w3.org&#x2f;2001&#x2f;XMLSchema-instance"
    xmlns="https&#x3a;&#x2f;&#x2f;analysiscenter.veracode.com&#x2f;schema&#x2f;4.0&#x2f;buildinfo"
    xsi:schemaLocation="https&#x3a;&#x2f;&#x2f;analysiscenter.veracode.com&#x2f;
    schema&#x2f;4.0&#x2f;buildinfo https&#x3a;&#x2f;&#x2f;analysiscenter.veracode.com&#x2f;
    resource&#x2f;4.0&#x2f;buildinfo.xsd" buildinfo_version="1.5" account_id="testaccount_id"
    app_id="testapp_id" build_id="test_build_id"><build version="6 Oct 2022 Static" build_id="test_build_id"
    submitter="Test User" platform="Not Specified" lifecycle_stage="Not Specified"
    results_ready="false" policy_name="Test Policy" policy_version="11"
    policy_compliance_status="Pass" policy_updated_date="2022-10-06T11&#x3a;28&#x3a;03-04&#x3a;00"
    rules_status="Pass" grace_period_expired="false" scan_overdue="false"
    legacy_scan_engine="false">\n      <analysis_unit analysis_type="Static"
    status="Pre-Scan Failed"/>\n   </build>\n</buildinfo>\n"""


FAKE_GET_PRESCAN_SUCCESS = """<?xml version="1.0" encoding="UTF-8"?>\n\n<prescanresults
    xmlns:xsi="http&#x3a;&#x2f;&#x2f;www.w3.org&#x2f;2001&#x2f;XMLSchema-instance"
    xmlns="https&#x3a;&#x2f;&#x2f;analysiscenter.veracode.com&#x2f;schema&#x2f;2.0&#x2f;
    prescanresults" xsi:schemaLocation="https&#x3a;&#x2f;&#x2f;analysiscenter.veracode.com&#x2f;
    schema&#x2f;2.0&#x2f;prescanresults https&#x3a;&#x2f;&#x2f;analysiscenter.veracode.com&#x2f;
    resource&#x2f;2.0&#x2f;prescanresults.xsd" prescanresults_version="1.4"
    account_id="testaccount_id" app_id="testapp_id" build_id="test_build_id"><module id="test_module_id"
    name="Python Files" app_file_id="test_app_file_id" checksum="test_checksum"
    platform="Python &#x2f; Python" size="test_size" status="OK" has_fatal_errors="false"
    is_dependency="false" difference="unmodified">\n      <issue details="No supporting files or
    PDB files"/>\n   </module>\n</prescanresults>\n"""

FAKE_GET_PRESCAN_NOT_AVAIL = """<?xml version="1.0" encoding="UTF-8"?>\n\n<error>
    Prescan results not available for application&#x3d;testapp_id</error>\n"""

FAKE_BEGIN_SCAN_SUCCESS = """<?xml version="1.0" encoding="UTF-8"?>\n\n<buildinfo
    xmlns:xsi="http&#x3a;&#x2f;&#x2f;www.w3.org&#x2f;2001&#x2f;XMLSchema-instance"
    xmlns="https&#x3a;&#x2f;&#x2f;analysiscenter.veracode.com&#x2f;schema&#x2f;4.0&#x2f;buildinfo"
    xsi:schemaLocation="https&#x3a;&#x2f;&#x2f;analysiscenter.veracode.com&#x2f;
    schema&#x2f;4.0&#x2f;buildinfo https&#x3a;&#x2f;&#x2f;analysiscenter.veracode.com&#x2f;
    resource&#x2f;4.0&#x2f;buildinfo.xsd" buildinfo_version="1.5" account_id="testaccount_id"
    app_id="testapp_id" build_id="test_build_id"><build version="27 Sep 2022 Static &#x28;2&#x29;"
    build_id="test_build_id" submitter="Test User" platform="Not Specified"
    lifecycle_stage="Not Specified" results_ready="false" policy_name="Test-Policy"
    policy_version="6" policy_compliance_status="Calculating..."
    policy_updated_date="2022-09-27T15&#x3a;59&#x3a;57-04&#x3a;00" rules_status="Calculating..."
    grace_period_expired="false" scan_overdue="false" legacy_scan_engine="false">\n
    <analysis_unit analysis_type="Static" status="Submitted to Engine"
    engine_version="test_engine_version"/>\n   </build>\n</buildinfo>\n"""

FAKE_BEGIN_SCAN_ERROR = """<?xml version="1.0" encoding="UTF-8"?>\n\n
    <buildinfo xmlns:xsi="http&#x3a;&#x2f;&#x2f;www.w3.org&#x2f;2001&#x2f;XMLSchema-instance"
    xmlns="https&#x3a;&#x2f;&#x2f;analysiscenter.veracode.com&#x2f;schema&#x2f;4.0&#x2f;buildinfo"
    xsi:schemaLocation="https&#x3a;&#x2f;&#x2f;analysiscenter.veracode.com&#x2f;
    schema&#x2f;4.0&#x2f;buildinfo https&#x3a;&#x2f;&#x2f;analysiscenter.veracode.com&#x2f;
    resource&#x2f;4.0&#x2f;buildinfo.xsd" buildinfo_version="1.5" account_id="testaccount_id"
    app_id="testapp_id" build_id="test_build_id"><build version="27 Sep 2022 Static &#x28;2&#x29;"
    build_id="test_build_id" submitter="Test User" platform="Not Specified"
    lifecycle_stage="Not Specified" results_ready="false" policy_name="Test-Policy"
    policy_version="6" policy_compliance_status="Calculating..."
    policy_updated_date="2022-09-27T15&#x3a;59&#x3a;57-04&#x3a;00" rules_status="Calculating..."
    grace_period_expired="false" scan_overdue="false" legacy_scan_engine="false">\n
    <analysis_unit analysis_type="Static" status="not submitted to engine"
    engine_version="test_engine_version"/>\n   </build>\n</buildinfo>\n"""


class FakeResponse:
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text

    def test(self):
        return self.text

    def raise_for_status(self):
        if self.status_code >= 300:
            raise HTTPError(f"{self.status_code} Test HTTP Error", response=self)
