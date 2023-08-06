from unittest.mock import ANY
from unittest.mock import patch

import pytest
from pawapi import TaskInterval
from typer.testing import CliRunner

from pawcli.app import app

MODULE = "pawcli.commands.task"

runner = CliRunner()

task_id = 123456
new_command = "echo 'Hello Test!'"
new_description = "Foo"
upd_command = "echo '!Foo Bar'"
upd_description = "Bar"


@pytest.fixture(autouse=True)
def mock_process_result(monkeypatch, dummy):
    monkeypatch.setattr(f"{MODULE}.scheduled.process_result", dummy)
    monkeypatch.setattr(f"{MODULE}.alwayson.process_result", dummy)


@pytest.fixture(autouse=True)
def mock_get_api(monkeypatch, dummy):
    monkeypatch.setattr(f"{MODULE}.scheduled.init_api", dummy)
    monkeypatch.setattr("pawcli.app.scheduled_app.info.callback", None)


def test_aon_ls(mock_api):
    result = runner.invoke(app, ["task", "aon", "ls"])
    assert result.exit_code == 0, result.stdout
    mock_api.alwayson_task.list.assert_called_once()


def test_aon_new_error_command_is_required(mock_api):
    result = runner.invoke(app, ["task", "aon", "new"])
    assert result.exit_code != 0, result.stdout
    assert "Missing argument" in result.stdout
    mock_api.alwayson_task.create.assert_not_called()


def test_aon_new_command(mock_api):
    result = runner.invoke(app, ["task", "aon", "new", new_command])
    assert result.exit_code == 0, result.stdout
    mock_api.alwayson_task.create.assert_called_once_with(
        command=new_command,
        enabled=None,
        description=None,
    )


def test_aon_new_command_enable(mock_api):
    result = runner.invoke(app, ["task", "aon", "new", new_command, "--enable"])
    assert result.exit_code == 0, result.stdout
    mock_api.alwayson_task.create.assert_called_once_with(
        command=new_command,
        enabled=True,
        description=None,
    )


def test_aon_new_all(mock_api):
    result = runner.invoke(
        app, [
            "task", "aon", "new",
            new_command,
            "--enable",
            "-d", new_description,
        ],
    )  # yapf: disable
    assert result.exit_code == 0, result.stdout
    mock_api.alwayson_task.create.assert_called_once_with(
        command=new_command,
        enabled=True,
        description=new_description,
    )


def test_aon_new_command_disable(mock_api):
    result = runner.invoke(
        app, ["task", "aon", "new", new_command, "--disable"]
    )
    assert result.exit_code == 0, result.stdout
    mock_api.alwayson_task.create.assert_called_once_with(
        command=new_command,
        enabled=False,
        description=None,
    )


def test_aon_update_command_disable(mock_api):
    result = runner.invoke(
        app, [
            "task", "aon", "update", str(task_id),
            "--disable",
            "--command", upd_command,
        ],
    )  # yapf: disable
    assert result.exit_code == 0, result.stdout
    mock_api.alwayson_task.update.assert_called_once_with(
        task_id=task_id,
        command=upd_command,
        enabled=False,
        description=None,
    )


def test_aon_info(mock_api):
    result = runner.invoke(app, ["task", "aon", "info", str(task_id)])
    assert result.exit_code == 0, result.stdout
    mock_api.alwayson_task.get_info.assert_called_once_with(task_id)


def test_aon_rm(mock_api):
    result = runner.invoke(app, ["task", "aon", "rm", str(task_id)])
    assert result.exit_code == 0, result.stdout
    mock_api.alwayson_task.delete.assert_called_once_with(task_id)


def test_aon_rm_id_missing(mock_api):
    result = runner.invoke(app, ["task", "aon", "rm"])
    assert result.exit_code != 0, result.stdout
    assert "Missing argument" in result.stdout
    mock_api.alwayson_task.delete.assert_not_called()


def test_ls(mock_api):
    result = runner.invoke(app, ["task", "ls"])
    assert result.exit_code == 0, result.stdout
    mock_api.scheduled_task.list.assert_called_once()


def test_new_error_command(mock_api):
    result = runner.invoke(app, ["task", "new"])
    assert result.exit_code != 0, result.stdout
    assert "Missing argument" in result.stdout


def test_new_command(mock_api):
    result = runner.invoke(app, ["task", "new", new_command])
    assert result.exit_code == 0, result.stdout
    mock_api.scheduled_task.create.assert_called_once_with(
        command=new_command,
        minute=0,
        hour=0,
        enabled=None,
        interval=TaskInterval.DAILY,
        description=None,
    )


def test_new_all_enable_hourly(mock_api):
    result = runner.invoke(
        app, [
            "task", "new",
            new_command,
            "-d", new_description,
            "--enable",
            "--minute", "15",
            "--interval", "hourly",
        ],
    )  # yapf: disable
    assert result.exit_code == 0, result.stdout
    mock_api.scheduled_task.create.assert_called_once_with(
        command=new_command,
        minute=15,
        hour=0,
        enabled=True,
        interval=TaskInterval.HOURLY,
        description=new_description,
    )


def test_new_all_enable_daily(mock_api):
    result = runner.invoke(
        app, [
            "task", "new",
            new_command,
            "-d", new_description,
            "--enable",
            "--minute", "15",
            "--hour", "12",
            "--interval", "daily",
        ],
    )  # yapf: disable
    assert result.exit_code == 0, result.stdout
    mock_api.scheduled_task.create.assert_called_once_with(
        command=new_command,
        minute=15,
        hour=12,
        enabled=True,
        interval=TaskInterval.DAILY,
        description=new_description,
    )


def test_update_all_disable_daily(mock_api):
    result = runner.invoke(
        app, [
            "task", "update", str(task_id),
            "--disable",
            "-d", upd_description,
            "-c", upd_command,
            "--minute", "12",
            "--hour", "15",
            "--interval", "daily",
        ],
    )  # yapf: disable
    assert result.exit_code == 0, result.stdout
    mock_api.scheduled_task.update.assert_called_once_with(
        task_id=task_id,
        command=upd_command,
        minute=12,
        hour=15,
        enabled=False,
        interval=TaskInterval.DAILY,
        description=upd_description,
    )


def test_update_all_invalid_enum(mock_api):
    result = runner.invoke(
        app, [
            "task", "update", str(task_id),
            "--interval", "invalid",
        ],
    )  # yapf: disable
    assert result.exit_code != 0, result.stdout
    assert "Invalid value" in result.stdout
    mock_api.scheduled_task.update.assert_not_called()


@pytest.mark.parametrize("hour", (-1, 24))
def test_update_all_invalid_hour(mock_api, hour):
    result = runner.invoke(
        app, [
            "task", "update", str(task_id),
            "--hour", hour,
        ],
    )  # yapf: disable
    assert result.exit_code != 0, result.stdout
    assert "Invalid value" in result.stdout
    mock_api.scheduled_task.update.assert_not_called()


@pytest.mark.parametrize("minute", (-1, 60))
def test_update_all_invalid_minute(mock_api, minute):
    result = runner.invoke(
        app, [
            "task", "update", str(task_id),
            "--minute", minute,
        ],
    )  # yapf: disable
    assert result.exit_code != 0, result.stdout
    assert "Invalid value" in result.stdout
    mock_api.scheduled_task.update.assert_not_called()


def test_update_all_missing_option_value(mock_api):
    result = runner.invoke(app, ["task", "update", str(task_id), "--minute"])
    assert result.exit_code != 0, result.stdout
    assert "requires an argument" in result.stdout
    mock_api.scheduled_task.update.assert_not_called()


def test_info(mock_api):
    result = runner.invoke(app, ["task", "info", str(task_id)])
    assert result.exit_code == 0, result.stdout
    mock_api.scheduled_task.get_info.assert_called_once_with(task_id)


def test_rm(mock_api):
    result = runner.invoke(app, ["task", "rm", str(task_id)])
    assert result.exit_code == 0, result.stdout
    mock_api.scheduled_task.delete.assert_called_once_with(task_id)


def test_cat(mock_api):
    with patch(f"{MODULE}.scheduled.cat") as mock_cat:
        result = runner.invoke(app, ["task", "log", "123456"])
    assert result.exit_code == 0, result.stdout
    mock_cat.assert_called_once_with(ANY, "/var/log/schedule-log-123456.log")


def test_aon_cat(mock_api):
    with patch(f"{MODULE}.alwayson.cat") as mock_cat:
        result = runner.invoke(app, ["task", "aon", "log", "123456"])
    assert result.exit_code == 0, result.stdout
    mock_cat.assert_called_once_with(ANY, "/var/log/alwayson-log-123456.log")
