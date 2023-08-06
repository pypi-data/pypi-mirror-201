import unittest.mock as mock

import pytest


@pytest.fixture(autouse=True)
def reset_mock_api(mock_api):
    mock_api.reset_mock()


@pytest.fixture(scope="module")
def mock_ContextObject(mock_context_object):
    obj = mock.Mock()
    obj.return_value = mock_context_object
    return obj


@pytest.fixture(autouse=True)
def mock_replace_context_obj(monkeypatch, mock_ContextObject):
    monkeypatch.setattr(
        "pawcli.core.callback.ContextObject", mock_ContextObject
    )
