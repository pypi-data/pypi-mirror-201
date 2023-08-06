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

import pytest
from security_scan_invoker.parser import Parser
from .fake_arg_parser import FakeArgParser


# pylint: disable=too-many-instance-attributes, too-many-arguments
class TestArgs:
    def __init__(
            self,
            appname: list,
            version: list,
            vid: str,
            vkey: str,
            filepath: str,
            select_previous_modules: str = ""):
        self.appname = appname
        self.version = version
        self.vid = vid
        self.vkey = vkey
        self.filepath = filepath
        self.select_previous_modules = select_previous_modules


class TestParser:

    @staticmethod
    def test_parse_throws_system_exit_if_unable_to_parse():
        fake_arg_parser = FakeArgParser(None)

        with pytest.raises(SystemExit):
            Parser(fake_arg_parser).parse()

    @staticmethod
    def test_parse_throws_system_exit_if_parsed_vals_are_empty():
        fake_arg_parser = FakeArgParser(TestArgs(None, None, None, None, None, None))

        with pytest.raises(SystemExit):
            Parser(fake_arg_parser).parse()

    @staticmethod
    def test_parse_adds_args():
        fake_arg_parser = FakeArgParser(TestArgs([], [], "", "", "", ""))

        try:
            Parser(fake_arg_parser).parse()
        # Throw a sys exit because we don't actually give it args
        except SystemExit:
            pass

        assert len(list(filter(lambda arg: "--vid" in arg, fake_arg_parser.args))) == 1
        assert len(list(filter(lambda arg: "--vkey" in arg, fake_arg_parser.args))) == 1
        assert (
            len(list(filter(lambda arg: "--appname" in arg, fake_arg_parser.args))) == 1
        )
        assert (
            len(list(filter(lambda arg: "--version" in arg, fake_arg_parser.args)))
            == 1
        )
        assert (
            len(list(filter(lambda arg: "--filepath" in arg, fake_arg_parser.args)))
            == 1
        )
        assert (
            len(list(filter(lambda arg: "--select_previous_modules" in arg,
                            fake_arg_parser.args))) == 1)

    @staticmethod
    def test_parse_returns_parsed_args():
        expected_parsed_app_name = "test_parsed_app_name"
        expected_parsed_version = "test_parsed_version"
        expected_vid = "testvid"
        expected_vkey = "testvkey"
        expected_filepath = " testpluginpackage"
        parsed_arg_to_return = TestArgs(
            appname=[expected_parsed_app_name],
            version=[expected_parsed_version],
            vid=expected_vid,
            vkey=expected_vkey,
            filepath=expected_filepath,
        )

        parsed_args = Parser(FakeArgParser(parsed_arg_to_return)).parse()

        assert expected_parsed_app_name == parsed_args.app_name
        assert expected_parsed_version == parsed_args.version
        assert expected_vid == parsed_args.vid
        assert expected_vkey == parsed_args.vkey
        assert expected_filepath == parsed_args.filepath

    @staticmethod
    def test_parse_handles_spaces_in_appname():
        fake_arg_parser = FakeArgParser(
            TestArgs(["one", "two", "three"], [""], "test", "test", "test", "test"))

        parsed_args = Parser(fake_arg_parser).parse()

        list_of_dicts_with_appname = list(
            filter(lambda arg: "--appname" in arg, fake_arg_parser.args)
        )
        assert len(list_of_dicts_with_appname) == 1
        assert "nargs" in list_of_dicts_with_appname[0]["--appname"]
        assert list_of_dicts_with_appname[0]["--appname"]["nargs"] == "+"
        assert parsed_args.app_name == "one two three"

    @staticmethod
    def test_parse_handles_spaces_in_version():
        fake_arg_parser = FakeArgParser(
            TestArgs([""], ["one", "two", "three"], "test", "test", "test", "test"))

        parsed_args = Parser(fake_arg_parser).parse()

        list_of_dicts_with_version = list(
            filter(lambda arg: "--version" in arg, fake_arg_parser.args)
        )
        assert len(list_of_dicts_with_version) == 1
        assert "nargs" in list_of_dicts_with_version[0]["--version"]
        assert list_of_dicts_with_version[0]["--version"]["nargs"] == "+"
        assert parsed_args.version == "one two three"
