"""fmf_tools.py: Module to manipulate FMF."""

import os
from fmf import Tree
import fmf.utils
import rdmaqe


def get_rdmaqe_path():
    rdmaqe_path = rdmaqe.__file__
    return rdmaqe_path.replace("__file__", "")


def get_dir_from_name(name):
    if not os.path.isdir(get_rdmaqe_path() + "/tests/" + name):
        return "/".join(name.split("/")[:-1])
    return name


def get_tree():
    """
    Returns FMF Tree object initialized in rdmaqe tests root directory.
    :return:
    :rtype Tree
    :return: FMF Tree object with root in rdmaqe tests path
    """
    path = get_rdmaqe_path() + "/tests/"
    return Tree(path)


def get_tests_path(name):
    return get_rdmaqe_path() + "/tests/" + get_dir_from_name(name)


def get_test_name(tree):
    test_path = tree.get("test")
    if test_path.startswith("/"):
        return test_path
    remove, test_path = correct_path(test_path)
    return "/".join(tree.name.split("/")[1 : -(1 + remove)]) + "/" + test_path


def correct_path(path):
    # Sometimes there is '../$path' in path, we need get number of these and remove them from the path
    remove = 0
    while "../" in path:
        path = "/".join(path.split("/")[1:])
        remove += 1
    return remove, path


def fmf_filter(filter, node):
    try:
        return fmf.utils.filter(filter=filter, data=node)
    except fmf.utils.FilterError:
        # If the attribute is missing, return as not found
        return False


def filter_tree(filters, name=None, verbose=False, to_print=False):
    # returns list of tests filtered by given filter
    #         "tier:1 & test:this.py" --> all tests that run 'this.py' on tier 1
    #         "tier:1 | test:this.py" --> all tests that run 'this.py' or are on tier 1
    # verbose True: returns list of dicts of test metadata
    #         False: return list of strings of test names

    if not isinstance(filters, list):
        raise fmf.utils.FilterError("Invalid filter '%s'" % type(filters))
    for f in filters:
        if not isinstance(f, str):
            raise fmf.utils.FilterError("Invalid filter '%s'" % type(f))
    tree = get_tree()
    filtered = []
    for leaf in tree.climb():
        # skip test that doesn't contain string specified with 'name' parameter
        if name is not None and name not in leaf.show(brief=True):
            continue
        try:
            if not all([fmf_filter(filter=f, node=leaf.data) for f in filters]):
                continue
        # Handle missing attribute as if filter failed
        except fmf.utils.FilterError:
            continue
        if not verbose:
            filtered.append(leaf.show(brief=True))
        else:
            if to_print:
                filtered.append(dict(leaf.show()))
            else:
                filtered.append(dict(leaf.data))
    return filtered
