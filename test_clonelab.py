import pytest
import os
import load
from clonelab import ssh_key_import
from clonelab import ssh_config_import
from clonelab import check_ssh_path


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


def test_ssh_key_import():
    private_key = "example private key"
    public_key = "example public key"
    assert ssh_key_import(private_key, public_key) == True


def test_ssh_config_import():
    config = "this is an example ssh config file"
    assert ssh_config_import(config) == True


def test_check_ssh_path():
    assert check_ssh_path() == 0


main()