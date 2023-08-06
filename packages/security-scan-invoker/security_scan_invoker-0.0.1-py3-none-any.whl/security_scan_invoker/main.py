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

import logging.config
import os
from .veracode_scanner_app import VeracodeScannerApp
from .arg_parser_wrapper import ArgParserWrapper
from .parser import Parser
from .scanner_args import ScannerArgs
from .veracode_api_wrapper import VeracodeAPIWrapper
from .build_details_fetcher import BuildDetailsFetcher


def main():
    """Runs the Security Scan Invoker process.
    Will parse arguments given and use those to check and launch scans.
    """

    configure_logging()
    args: ScannerArgs = Parser(ArgParserWrapper()).parse()

    run_veracode_scanner_app(args)


def run_veracode_scanner_app(args: ScannerArgs) -> int:
    """Runs the Security Scan Invoker app with the arguments given

    :param args: The args to use when running the app
    :type args: ScannerArgs
    :return: The exit code of the app. 0 if successful, 1 if an error, and 101 if no new scan
        is needed.
    :rtype: int
    """
    veracode_api_wrapper = VeracodeAPIWrapper(args.vid, args.vkey)
    build_details_fetcher = BuildDetailsFetcher(veracode_api_wrapper)

    return VeracodeScannerApp(args, build_details_fetcher, veracode_api_wrapper).run()


def configure_logging():
    """Configures logging for the app using the specified logging configuration
    """
    log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logging.conf')
    logging.config.fileConfig(log_file_path)


if __name__ == "__main__":
    main()
