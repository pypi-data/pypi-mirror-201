import rdmaqe
from fmf import Tree

def get_rdmaqe_path():
    _rdmaqe_path = rdmaqe.__file__
    rdmaqe_path = _rdmaqe_path.replace("__init__.py", "")
    return rdmaqe_path

rdmaqe_path = get_rdmaqe_path()
_IN_TREE_TESTS_DIR = rdmaqe_path + "tests/"

def main():
    test_dir = _IN_TREE_TESTS_DIR
    print(test_dir)
    print(Tree(test_dir))


if __name__ == "__main__":
    main()


