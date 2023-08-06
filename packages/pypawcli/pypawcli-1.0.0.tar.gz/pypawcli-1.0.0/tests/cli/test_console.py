import unittest.mock as mock

import pytest
from pawapi import Shell
from typer.testing import CliRunner

from pawcli.app import app

MODULE = "pawcli.commands.console"

runner = CliRunner()

console_id = 98765
cmd_command = "echo 'Hello World'"
cmd_command_nl = cmd_command + "\n"


@pytest.fixture(autouse=True)
def mock_process_result(monkeypatch, dummy):
    monkeypatch.setattr(f"{MODULE}.process_result", dummy)


@pytest.fixture(autouse=True)
def mock_file_get_api(monkeypatch, dummy):
    monkeypatch.setattr(f"{MODULE}.init_api", dummy)
    monkeypatch.setattr("pawcli.app.console_app.info.callback", None)


def test_ls(mock_api):
    result = runner.invoke(app, ["console", "ls"])
    assert result.exit_code == 0, result.stdout
    mock_api.console.list.assert_called_once()


def test_ls_shared(mock_api):
    result = runner.invoke(app, ["console", "ls", "--shared"])
    assert result.exit_code == 0, result.stdout
    mock_api.console.list_shared.assert_called_once()


@pytest.mark.parametrize(
    "cli,args",
    (
        (
            ["bash", "--args", "--norc"],
            dict(
                executable=Shell.BASH,
                arguments="--norc",
                working_directory=None,
            ),
        ),
        (
            ["pypy3", "-d", "~/src"],
            dict(
                executable=Shell.PYPY3,
                arguments=None,
                working_directory="/home/{}/src",
            ),
        ),
    ),
)
def test_new(mock_api, cli, args, username):
    wd = args["working_directory"]
    if wd is not None:
        args["working_directory"] = wd.format(username)

    result = runner.invoke(app, ["console", "new", *cli])
    assert result.exit_code == 0, result.stdout
    mock_api.console.create.assert_called_once_with(**args)


def test_new_as_default(monkeypatch, mock_context_object):
    new_console_id = 200100
    resp = mock.Mock()
    resp.content = {"id": new_console_id}
    mock_context_object.api.console.create.return_value = resp
    monkeypatch.delitem(mock_context_object.config["console"], "default_id")
    with mock.patch(f"{MODULE}.save_config") as save_config:
        result = runner.invoke(app, ["console", "new", "bash", "--default"])
    assert result.exit_code == 0, result.stdout
    save_config.assert_called()
    mock_context_object.api.console.create.assert_called_once_with(
        executable=Shell.BASH,
        arguments=None,
        working_directory=None,
    )
    assert int(
        mock_context_object.config["console"]["default_id"]
    ) == new_console_id


def test_new_open(mock_context_object):
    resp = mock.Mock()
    url = "/user/username/consoles/1234/frame/"
    resp.content = {"console_frame_url": url}
    mock_context_object.api.console.create.return_value = resp
    with mock.patch(f"{MODULE}.launch") as launch:
        result = runner.invoke(app, ["console", "new", "bash", "--open"])
    assert result.exit_code == 0, result.stdout
    launch.assert_called_once_with(f"https://www.pythonanywhere.com{url}")
    mock_context_object.api.console.create.assert_called_once_with(
        executable=Shell.BASH,
        arguments=None,
        working_directory=None,
    )


def test_info(mock_api):
    id_ = 102030
    result = runner.invoke(app, ["console", "info", str(id_)])
    assert result.exit_code == 0, result.stdout
    mock_api.console.get_info.assert_called_once_with(id_)


def test_info_default_id(mock_api, mock_context_object):
    result = runner.invoke(app, ["console", "info"])
    assert result.exit_code == 0, result.stdout
    mock_api.console.get_info.assert_called_once_with(
        int(mock_context_object.config["console"]["default_id"])
    )


def test_rm(mock_api):
    result = runner.invoke(app, ["console", "rm", str(console_id)])
    assert result.exit_code == 0, result.stdout
    mock_api.console.kill.assert_called_once_with(console_id)


def test_rm_config_default(monkeypatch, mock_context_object):
    default_id = 9898980
    monkeypatch.setitem(
        mock_context_object.config["console"], "default_id", str(default_id)
    )
    with mock.patch(f"{MODULE}.save_config") as save_config:
        result = runner.invoke(app, ["console", "rm", str(default_id)])
    assert result.exit_code == 0, result.stdout
    save_config.assert_called_once()
    mock_context_object.api.console.kill.assert_called_once_with(default_id)
    assert mock_context_object.config.get(
        "console", "default_id", fallback=None
    ) is None


def test_output(mock_api):
    result = runner.invoke(app, ["console", "output", str(console_id)])
    assert result.exit_code == 0, result.stdout
    mock_api.console.get_output.assert_called_once_with(console_id)


def test_exec(mock_api):
    result = runner.invoke(
        app, ["console", "exec", "-c", str(console_id), cmd_command]
    )
    assert result.exit_code == 0, result.stdout
    mock_api.console.send_input.assert_called_once_with(
        console_id=console_id,
        input_=cmd_command_nl,
    )


def test_exec_default_id(mock_api, config_dict):
    result = runner.invoke(app, ["console", "exec", cmd_command])
    assert result.exit_code == 0, result.stdout
    mock_api.console.send_input.assert_called_once_with(
        console_id=int(config_dict["console"]["default_id"]),
        input_=cmd_command_nl,
    )


def test_exec_nl(mock_api):
    result = runner.invoke(
        app, ["console", "exec", "-c", str(console_id), cmd_command_nl]
    )
    assert result.exit_code == 0, result.stdout
    mock_api.console.send_input.assert_called_once_with(
        console_id=console_id,
        input_=cmd_command_nl,
    )
