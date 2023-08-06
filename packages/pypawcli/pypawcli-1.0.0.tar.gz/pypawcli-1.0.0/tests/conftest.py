import unittest.mock as mock

import pytest

from pawcli.core.config import Config
from pawcli.core.context import Credentials


@pytest.fixture(scope="module")
def mock_api():
    return mock.MagicMock()


@pytest.fixture(scope="module")
def mock_context_object(
    username, token, mock_api, config_dict, dummy, tmp_app_dir
):
    Config.read = dummy
    config = Config()
    config.read_dict(config_dict)
    config.file = tmp_app_dir / "config.ini"

    obj = mock.MagicMock()
    obj.credentials = Credentials(username=username, token=token)
    obj.api = mock_api
    obj.config = config

    return obj


@pytest.fixture(scope="session")
def dummy():
    return lambda *_, **__: None


@pytest.fixture(scope="session")
def username() -> str:
    return "foo"


@pytest.fixture(scope="session")
def token() -> str:
    return "foobar"


@pytest.fixture(scope="session")
def config_dict(token, username):
    return {
        "api": {
            "token": token,
            "username": username,
        },
        "console": {
            "default_id": "100200",
        },
        "webapp": {
            "default_domain": "foobar.baz",
        },
    }


@pytest.fixture(scope="session")
def tmp_app_dir(tmp_path_factory):
    dir = tmp_path_factory.mktemp("app_test")
    return dir
