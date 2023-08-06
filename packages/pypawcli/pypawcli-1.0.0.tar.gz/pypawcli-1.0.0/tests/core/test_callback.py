import unittest.mock as mock

import pytest
from pawapi.exceptions import InvalidCredentialsError
from pawapi.region import Region
from typer import Exit

from pawcli.core.callback import init_api
from pawcli.core.callback import init_context_object

MODULE = "pawcli.core.callback"


def test_init_context_object_config(mock_context_object):
    ctx = mock.MagicMock()
    with mock.patch(f"{MODULE}.Config") as config:
        config.return_value = mock_context_object.config

        init_context_object(
            ctx=ctx,
            username=None,
            token=None,
            region=None,
            config_file=None,
            timeout=None,
            version=False,
        )

    assert ctx.obj.credentials.token == mock_context_object.credentials.token
    assert ctx.obj.credentials.username == mock_context_object.credentials.username  # noqa: E501
    assert ctx.obj.credentials.region == mock_context_object.credentials.region


def test_init_context_object_cli(mock_context_object):
    ctx = mock.Mock()
    with mock.patch(f"{MODULE}.Config") as config:
        config.return_value = mock_context_object.config

        init_context_object(
            ctx=ctx,
            username="usernameCli",
            token="tokenCli",
            region=Region.EU,
            config_file=None,
            timeout=None,
            version=False,
        )

    assert ctx.obj.credentials.token == "tokenCli"
    assert ctx.obj.credentials.username == "usernameCli"
    assert ctx.obj.credentials.region is Region.EU


@pytest.fixture
def context(mock_context_object):
    ctx = mock.Mock()
    ctx.obj = mock_context_object
    ctx.exit.side_effect = Exit
    ctx.parent.params.get.return_value = None
    return ctx


def test_init_api(context):
    with mock.patch(f"{MODULE}.Pawapi") as pawapi:
        init_api(context)
        pawapi.assert_called_once_with(
            token=context.obj.credentials.token,
            username=context.obj.credentials.username,
            region=context.obj.credentials.region,
            timeout=float(context.obj.config._defaults["timeout"]),
        )


def test_init_api_timeout_cli(context):
    context.parent.params.get.return_value = 8.0
    with mock.patch(f"{MODULE}.Pawapi") as pawapi:
        init_api(context)
        pawapi.assert_called_once_with(
            token=context.obj.credentials.token,
            username=context.obj.credentials.username,
            region=context.obj.credentials.region,
            timeout=8.0,
        )


def test_init_api_timeout_config_error(monkeypatch, context):
    monkeypatch.setitem(context.obj.config["api"], "timeout", "str")
    with mock.patch(f"{MODULE}.Pawapi"):
        with pytest.raises(Exit):
            init_api(context)


def test_init_api_error(context):
    with mock.patch(f"{MODULE}.Pawapi") as pawapi:
        pawapi.side_effect = InvalidCredentialsError()
        with pytest.raises(Exit):
            init_api(context)
