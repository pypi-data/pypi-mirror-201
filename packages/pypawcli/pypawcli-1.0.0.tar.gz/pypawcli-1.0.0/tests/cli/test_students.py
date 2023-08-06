import pytest
from typer.testing import CliRunner

from pawcli.app import app

MODULE = "pawcli.commands.students"

runner = CliRunner()


@pytest.fixture(autouse=True)
def mock_process_result(monkeypatch, dummy):
    monkeypatch.setattr(f"{MODULE}.process_result", dummy)


@pytest.fixture(autouse=True)
def mock_students_get_api(monkeypatch):
    monkeypatch.setattr("pawcli.app.students_app.info.callback", None)


def test_ls(mock_api):
    result = runner.invoke(app, ["students", "ls"])
    assert result.exit_code == 0
    mock_api.students.list.assert_called_once()


def test_rm(mock_api):
    student_id = "123456"
    result = runner.invoke(app, ["students", "rm", student_id])
    assert result.exit_code == 0
    mock_api.students.delete.assert_called_once_with(student_id)


def test_rm_id_missing(mock_api):
    result = runner.invoke(app, ["students", "rm"])
    assert result.exit_code != 0
    assert "Missing argument" in result.stdout
    mock_api.students.delete.assert_not_called()
