import os
from os import listdir

import argparse

from rdmaqe.common.fmf_tools import (
    filter_tree,
    get_rdmaqe_path,
)

rdmaqe_path = get_rdmaqe_path()
_IN_TREE_TESTS_DIR = rdmaqe_path + "tests/"


def _list_all_test_cases() -> None:
    """Print all test cases from IN_TREE_TESTS_DIR."""
    test_cases = _load_test_cases()
    print("INFO: Showing all test files")
    for tc in test_cases:
        print("--> %s" % tc)


def _load_test_cases() -> list:
    """Return a list with all test cases from IN_TREE_TESTS_DIR
    :return: List of test cases
    :rtype: list
    """
    supported_file_types = [".sh", ".py", ".pl"]
    exclude_filenames = ["__init__"]
    tests_dir = [x[0] for x in os.walk(_IN_TREE_TESTS_DIR)]

    test_cases = []
    # search for supported test files within the directory
    for test_dir in tests_dir:
        for output in listdir(test_dir):
            tmp = os.path.join(test_dir, output)
            if os.path.isfile(os.path.join(tmp)):
                filename, file_extension = os.path.splitext(tmp)
                _, basename = os.path.split(filename)
                if file_extension in supported_file_types and basename not in exclude_filenames:
                    filename = filename.replace(_IN_TREE_TESTS_DIR, "")
                    test_name = filename + file_extension
                    # add / to begin of the name to match what is returned by test config
                    # test_name = "/" + test_name
                    test_cases.append(test_name)
    return test_cases


def _strip_quotation_marks(args):
    """rhts-simple-test-run actually passes the value including quotation marks, example follows
    var="value" gets passed as var="value" instead of just var=value.

    :param args: ArgumentParser object to strip quotation mark from.
    :return: stripped args
    :rtype: ArgumentParser
    """

    def _strip_value(val):
        val = val.strip('"')
        return val.strip("'")

    arguments = args.__dict__
    for arg in arguments:
        if isinstance(arguments[arg], list):
            setattr(args, arg, [_strip_value(a) for a in arguments[arg]])
            continue
        if arguments[arg] is None or not isinstance(arguments[arg], str):
            continue
        # Dynamically set the attribute to correct value
        setattr(args, arg, _strip_value(arguments[arg]))
    return args


def main():
    parser = argparse.ArgumentParser(description="rdmaqe-test", prog='rdmaqe-test')
    subparsers = parser.add_subparsers(help="Valid commands", dest="command")
    parser_list = subparsers.add_parser("list")
    parser_list.add_argument("type", choices=["tests", "configs"], type=str, default=False)
    # in case we want to list test cases from specific test config
    parser_list.add_argument("--config", "-c", required=False, dest="config", default=None, help="Test config file")
    parser_list.add_argument("--fmf", required=False, dest="fmf", default=False, action="store_true", help="Use fmf.")
    parser_list.add_argument(
        "--filter",
        "-f",
        required=False,
        dest="filter",
        type=str,
        default=list(""),
        help="(FMF) String of filters.",
        action="append",
    )
    parser_list.add_argument(
        "--path", required=False, dest="path", default="", help="(FMF) Relative path from stqe/tests/"
    )
    parser_list.add_argument(
        "--verbose",
        "-v",
        required=False,
        dest="verbose",
        default=False,
        action="store_true",
        help="(FMF) Be more verbose.",
    )

    args = _strip_quotation_marks(parser.parse_args())

    if args.command == "list":
        if args.type == "tests":
            if args.fmf:
                # List tests using fmf metadata in directory rdmaqe/tests/args.path
                tests = filter_tree(name=args.path, filters=args.filter, verbose=args.verbose, to_print=True)
                for test in tests:
                    print(test)
            elif not args.config:
                _list_all_test_cases()


if __name__ == "__main__":
    main()

