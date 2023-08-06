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

from security_scan_invoker.iface_arg_parser import IArgParser
from security_scan_invoker.scanner_args import ScannerArgs


class Parser:
    def __init__(self, arg_parser):
        self.arg_parser: IArgParser = arg_parser

    def parse(self) -> ScannerArgs:
        self.arg_parser.add_argument("--vid", help="API ID Generated from Veracode Platform "
                                                   "https://docs.veracode.com/r/t_create_api_creds")
        self.arg_parser.add_argument("--vkey", help="API KEY Generated from Veracode Platform "
                                     "https://docs.veracode.com/r/t_create_api_creds")
        self.arg_parser.add_argument(
            "--appname", help="App name in Veracode", nargs="+"
        )
        self.arg_parser.add_argument(
            "--version", help="Name or version of the build that you want to scan.", nargs="+"
        )
        self.arg_parser.add_argument("--filepath",
                                     help="Filepath of the package to be scanned")

        # Optional args
        self.arg_parser.add_argument("--select_previous_modules",
                                     help="Optional. Set to true to scan only the modules "
                                     "selected in the previous scan.")

        args = self.arg_parser.parse_args()
        Parser._check_required_args(args)
        args.appname = " ".join(args.appname)
        args.version = " ".join(args.version)
        args_dict = Parser._args_to_dict(args)
        return ScannerArgs(args_dict)

    @staticmethod
    def _args_to_dict(args) -> dict:
        """Converts the arguments given to a dictionary to be passed in for the ScannerArgs

        :param args: The parsed arguments to convert
        :type args: any
        :return: Python dictionary containing the arguments
        :rtype: dict
        """
        return {
            "appname": args.appname,
            "version": args.version,
            "vkey": args.vkey,
            "vid": args.vid,
            "filepath": args.filepath,
            "select_previous_modules": args.select_previous_modules
        }

    @staticmethod
    def _check_required_args(args):
        """Checks the required arguments to ensure needed fields have values.

        :param args: The arguments to verify
        :type args: any
        :raises SystemExit: If there are fields missing
        """

        message = ""
        if not hasattr(args, 'vid') or not args.vid:
            message += "Veracode ID (--vid) must be defined\n"

        if not hasattr(args, 'vkey') or not args.vkey:
            message += "Veracode key (--vkey) must be defined\n"

        if not hasattr(args, 'appname') or not args.appname:
            message += "Veracode application name (--appname) must be defined\n"

        if not hasattr(args, 'filepath') or not args.filepath:
            message += "Filepath (--filepath) must be defined\n"

        if not hasattr(args, 'version') or not args.version:
            message += "Version (--version) must be defined\n"

        if message:
            raise SystemExit(message)
