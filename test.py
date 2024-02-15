import pytest
import os
import git
import load

if os.getenv('_PYTEST_RAISE', "0") != "0":

    @pytest.hookimpl(tryfirst=True)
    def pytest_exception_interact(call):
        raise call.excinfo.value

    @pytest.hookimpl(tryfirst=True)
    def pytest_internalerror(excinfo):
        raise excinfo.value


def main():
    load.export_examples("/home/CloneLab/code/CloneLab")
    print("Done")




def test_export_examples():
    assert load.export_examples("/home/CloneLab/code/CloneLab") == 1



main()