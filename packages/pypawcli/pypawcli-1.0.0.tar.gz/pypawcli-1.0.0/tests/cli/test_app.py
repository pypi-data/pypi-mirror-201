from typer.testing import CliRunner

from pawcli.app import app
from pawcli.core.config import APP_NAME
from pawcli.version import __version__

runner = CliRunner()


def test_app_version() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0, result.stdout
    assert APP_NAME in result.stdout
    assert __version__ in result.stdout
