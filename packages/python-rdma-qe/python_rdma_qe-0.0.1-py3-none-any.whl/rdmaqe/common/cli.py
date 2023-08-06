"""cmdline.py: Module to execute command line."""

__author__ = "Zhaojuan Guo"
__copyright__ = "Copyright (c) 2023 Red Hat, Inc. All rights reserved."

from libsan.host.cmdline import run
from libsan import _print


def run_cli(cli=None):
    """
    Run a command line.
    :param cli:
    :return: The retcode and output of the command line
    """
    if not cli:
        _print("FAIL: run_cli() requires a command line as parameter.")
        return False, None

    retcode, output = run(cli, return_output=True, verbose=True)
    if retcode != 0:
        _print("FAIL: Could not run %s" % cli)
        return None

    return retcode, output

