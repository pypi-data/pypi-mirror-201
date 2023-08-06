import unittest.mock as mock

import pytest
from typer.testing import CliRunner

from pawcli.app import app

runner = CliRunner()


def test_get():
    result = runner.invoke(app, ["config", "api.username"])
    assert result.exit_code == 0
    assert "api.username" in result.stdout


def test_get_wrong_section():
    result = runner.invoke(app, ["config", "foo.python"])
    assert result.exit_code != 0, result.stdout
    assert "No section" in result.stdout


def test_get_missing_option():
    result = runner.invoke(app, ["config", "webapp.foo"])
    assert result.exit_code == 0, result.stdout
    assert "webapp.foo = <undefined>" in result.stdout


@pytest.mark.parametrize(
    "opt,value", (
        ("api.username", "user123"),
        ("console.default_id", 12345),
    )
)
def test_set(opt, value):
    with mock.patch("pawcli.app.save_config") as save_config:
        result = runner.invoke(app, ["config", opt, "--set", value])
        save_config.assert_called()

    assert result.exit_code == 0, result.stdout
    assert opt in result.stdout
    assert str(value) in result.stdout
