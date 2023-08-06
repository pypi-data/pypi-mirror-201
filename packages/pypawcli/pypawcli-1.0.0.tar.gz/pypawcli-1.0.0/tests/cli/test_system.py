import pytest
from pawapi import Python2
from pawapi import Python3
from pawapi import SystemImage
from typer.testing import CliRunner

from pawcli.app import app

MODULE = "pawcli.commands.system"

runner = CliRunner()


@pytest.fixture(autouse=True)
def mock_process_result(monkeypatch, dummy):
    monkeypatch.setattr(f"{MODULE}.process_result", dummy)


@pytest.fixture(autouse=True)
def mock_system_get_api(monkeypatch):
    monkeypatch.setattr("pawcli.app.system_app.info.callback", None)


def test_image_get(mock_api):
    result = runner.invoke(app, ["sys", "image"])
    assert result.exit_code == 0, result.stdout
    mock_api.system.get_current_image.assert_called_once()


@pytest.mark.parametrize("image", ("haggis", "dangermouse"))
def test_image_set(mock_api, image):
    result = runner.invoke(app, ["sys", "image", "--set", image])
    image_enum = SystemImage(image)
    assert result.exit_code == 0, result.stdout
    mock_api.system.set_version.assert_called_once_with(image_enum)


def test_py(mock_api):
    result = runner.invoke(app, ["sys", "py"])
    assert result.exit_code == 0, result.stdout
    mock_api.python.get_python_version.assert_called_once()


@pytest.mark.parametrize(
    "py,pyenum",
    (
        ("39", Python3.PYTHON39),
        ("37", Python3.PYTHON37),
        ("27", Python2.PYTHON27),
    )
)
def test_py_set(mock_api, py, pyenum):
    result = runner.invoke(app, ["sys", "py", "--set", py])
    assert result.exit_code == 0, result.stdout
    mock_api.python.set_python_version.assert_called_once_with(pyenum)


def test_py3(mock_api):
    result = runner.invoke(app, ["sys", "py3"])
    assert result.exit_code == 0, result.stdout
    mock_api.python.get_python3_version.assert_called_once()


@pytest.mark.parametrize(
    "py,pyenum", (
        ("39", Python3.PYTHON39),
        ("37", Python3.PYTHON37),
    )
)
def test_py3_set(mock_api, py, pyenum):
    result = runner.invoke(app, ["sys", "py3", "--set", py])
    assert result.exit_code == 0, result.stdout
    mock_api.python.set_python3_version.assert_called_once_with(pyenum)


def test_sar(mock_api):
    result = runner.invoke(app, ["sys", "sar"])
    assert result.exit_code == 0, result.stdout
    mock_api.python.get_sar_version.assert_called_once()


@pytest.mark.parametrize(
    "py,pyenum", (
        ("39", Python3.PYTHON39),
        ("37", Python3.PYTHON37),
    )
)
def test_sar_set(mock_api, py, pyenum):
    result = runner.invoke(app, ["sys", "sar", "--set", py])
    assert result.exit_code == 0, result.stdout
    mock_api.python.set_sar_version.assert_called_once_with(pyenum)


def test_cpu(mock_api):
    result = runner.invoke(app, ["sys", "cpu"])
    assert result.exit_code == 0, result.stdout
    mock_api.cpu.get_info.assert_called_once()
