"""roce.py: Module to check or configure OPA."""

__author__ = "Zhaojuan Guo"
__copyright__ = "Copyright (c) 2023 Red Hat, Inc. All rights reserved."

import libsan.host.linux
from libsan import _print
from libsan.host.cmdline import run


def opa_setup():
    """
    Make sure the subnet manager opafm service is running
    :return:
    True: If opafm service is running
    False: If not
    """
    print("INFO: Setting OPA fabric...")
    print("INFO: Installing subnet manager opa-fm...")

    if libsan.host.linux.service_status("opafm") != 0:
        opafm_install()
        print("INFO: Starting opafm service...")
        opafm_enable()
        if not opafm_restart():
            return False

    opaff_install()
    print("INFO: Querying OPA fabric info...")
    opafabricinfo()
    opasaquery()
    return True


def opafm_install():
    """
    Install opa-fm
    :return:
    True: If package is installed successfully
    False: If could not install package correctly
    """
    os_version = libsan.host.linux.dist_ver()
    if not os_version:
        return False

    opafm_package = "opa-fm"

    if not libsan.host.linux.install_package(opafm_package):
        _print("FAIL: Could not install %s" % opafm_package)
        return False

    return True


def opafm_enable():
    """
    Enable and start opafm service
    :return:
    True: If service is enabled
    False: If not
    """
    serv_name = "opafm"
    if not libsan.host.linux.service_enable(serv_name):
        _print("FAIL: Could not enable opafm service")
        return False

    libsan.host.linux.sleep(5)
    return True


def opafm_restart():
    """
    Restart opafm service
    :return:
    True: If opafm service started
    False: If did not start
    """
    serv_name = "opafm"
    if not libsan.host.linux.service_restart(serv_name):
        _print("FAIL: Could not restart opafm service")
        return False

    libsan.host.linux.sleep(5)
    return True


def opaff_install():
    """
        Install opa-ff
        :return:
        True: If package is installed successfully
        False: If could not install package correctly
        """
    os_version = libsan.host.linux.dist_ver()
    if not os_version:
        return False

    opafm_package = "opa-fastfabric"

    if not libsan.host.linux.install_package(opafm_package):
        _print("FAIL: Could not install %s" % opafm_package)
        return False

    return True


def opafabricinfo():
    """
    Query the fabric info
    :return: the fabric info
    """
    cmd = "/usr/sbin/opafabricinfo"
    retcode, output = run(cmd, return_output=True, verbose=True)
    if retcode != 0:
        _print("FAIL: Could not run opafabricinfo")
        return None

    return output


def opasaquery():
    """
    Performs various queries of the subnet manager/subnet agent and provides detailed fabric information
    :return:
    """
    cmd = "/usr/sbin/opasaquery"
    retcode, output = run(cmd, return_output=True, verbose=True)
    if retcode != 0:
        _print("FAIL: Could not run opasaquery")
        return None

    return output