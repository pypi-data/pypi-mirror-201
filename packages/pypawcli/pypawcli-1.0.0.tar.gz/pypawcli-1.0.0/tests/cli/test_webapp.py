import unittest.mock as mock
from pathlib import Path

import pytest
from pawapi import Python3
from typer.testing import CliRunner

from pawcli.app import app
from pawcli.commands.webapp.app import _setup_context

MODULE = "pawcli.commands.webapp"

runner = CliRunner()


@pytest.fixture(autouse=True)
def mock_process_result(monkeypatch, dummy):
    monkeypatch.setattr(f"{MODULE}.app.process_result", dummy)
    monkeypatch.setattr(f"{MODULE}.static.process_result", dummy)
    monkeypatch.setattr(f"{MODULE}.header.process_result", dummy)
    monkeypatch.setattr(f"{MODULE}.ssl.process_result", dummy)


@pytest.fixture(autouse=True)
def mock_get_api(monkeypatch, dummy):
    monkeypatch.setattr(f"{MODULE}.app.init_api", dummy)
    monkeypatch.setattr("pawcli.app.webapp_app.info.callback", None)


class TestSetupContext:

    @pytest.fixture
    def mock_context(self, mock_context_object):
        ctx = mock.Mock()
        ctx.obj = mock_context_object
        return ctx

    def test_setup_context_fallback_domain(self, monkeypatch, mock_context):
        monkeypatch.setitem(
            mock_context.obj.config["webapp"], "default_domain", ""
        )
        _setup_context(mock_context)
        username = mock_context.obj.credentials.username
        assert (
            mock_context.default_map["info"]["domain"]
        ) == f"{username}.pythonanywhere.com"

    def test_setup_context_default_domain(self, monkeypatch, mock_context):
        _setup_context(mock_context)
        domain = mock_context.obj.config["webapp"]["default_domain"]
        assert mock_context.default_map["info"]["domain"] == domain


def test_ls(mock_api):
    result = runner.invoke(app, ["app", "ls"])
    assert result.exit_code == 0, result.stdout
    mock_api.webapp.list.assert_called_once()


def test_info_fallback_domain(
    monkeypatch, mock_api, username, mock_context_object
):
    monkeypatch.setitem(
        mock_context_object.config["webapp"], "default_domain", ""
    )

    result = runner.invoke(app, ["app", "info"])
    assert result.exit_code == 0, result.stdout
    mock_api.webapp.get_info.assert_called_once_with(
        f"{username}.pythonanywhere.com"
    )


def test_info_default_domain(mock_api, config_dict):
    result = runner.invoke(app, ["app", "info"])
    assert result.exit_code == 0, result.stdout
    mock_api.webapp.get_info.assert_called_once_with(
        config_dict["webapp"]["default_domain"]
    )


def test_info_cli_domain(mock_api):
    result = runner.invoke(app, ["app", "info", "foo.bar"])
    assert result.exit_code == 0, result.stdout
    mock_api.webapp.get_info.assert_called_once_with("foo.bar")


def test_new_default(mock_api, config_dict):
    result = runner.invoke(app, ["app", "new"])
    assert result.exit_code == 0, result.stdout
    mock_api.webapp.create.assert_called_once_with(
        config_dict["webapp"]["default_domain"], Python3.PYTHON39
    )


def test_new_python38(mock_api, config_dict):
    result = runner.invoke(app, ["app", "new", "--py", "38"])
    assert result.exit_code == 0, result.stdout
    mock_api.webapp.create.assert_called_once_with(
        config_dict["webapp"]["default_domain"], Python3.PYTHON38
    )


def test_new_python38_domain(mock_api):
    result = runner.invoke(app, ["app", "new", "--py", "38", "bar.foo"])
    assert result.exit_code == 0, result.stdout
    mock_api.webapp.create.assert_called_once_with("bar.foo", Python3.PYTHON38)


def test_new_python38_domain_as_default(
    monkeypatch,
    mock_api,
    mock_context_object,
):
    monkeypatch.setitem(
        mock_context_object.config["webapp"], "default_domain", ""
    )

    with mock.patch(f"{MODULE}.app.save_config") as save_config:
        result = runner.invoke(
            app, ["app", "new", "--py", "38", "bar.foo", "--default"]
        )
    assert result.exit_code == 0, result.stdout
    save_config.assert_called()
    assert mock_context_object.config["webapp"]["default_domain"] == "bar.foo"
    mock_api.webapp.create.assert_called_once_with("bar.foo", Python3.PYTHON38)


def test_update_py(mock_api, config_dict):
    result = runner.invoke(app, ["app", "update", "--py", "310"])
    assert result.exit_code == 0, result.stdout
    mock_api.webapp.update.assert_called_once_with(
        domain_name=config_dict["webapp"]["default_domain"],
        python_version=Python3.PYTHON310,
        source_directory=None,
        virtualenv_path=None,
        force_https=None,
        protection=None,
        protection_username=None,
        protection_password=None,
    )


def test_update_py_src(mock_api, config_dict):
    result = runner.invoke(
        app, ["app", "update", "--py", "310", "--src", "~/foo"]
    )
    assert result.exit_code == 0, result.stdout
    mock_api.webapp.update.assert_called_once_with(
        domain_name=config_dict["webapp"]["default_domain"],
        python_version=Python3.PYTHON310,
        source_directory=f"/home/{config_dict['api']['username']}/foo",
        virtualenv_path=None,
        force_https=None,
        protection=None,
        protection_username=None,
        protection_password=None,
    )


def test_update_py_src_venv(mock_api, config_dict):
    result = runner.invoke(
        app,
        [
            "app", "update",
            "--py", "310",
            "--src", "~/foo",
            "--venv", "~/foo_venv",
        ],
    )  # yapf: disable
    assert result.exit_code == 0, result.stdout

    username = config_dict['api']['username']
    mock_api.webapp.update.assert_called_once_with(
        domain_name=config_dict["webapp"]["default_domain"],
        python_version=Python3.PYTHON310,
        source_directory=f"/home/{username}/foo",
        virtualenv_path=f"/home/{username}/foo_venv",
        force_https=None,
        protection=None,
        protection_username=None,
        protection_password=None,
    )


def test_update_py_src_venv_https(mock_api, config_dict):
    result = runner.invoke(
        app,
        [
            "app", "update",
            "--py", "310",
            "--src", "~/foo",
            "--venv", "~/foo_venv",
            "--https",
        ],
    )  # yapf: disable
    assert result.exit_code == 0, result.stdout

    username = config_dict['api']['username']
    mock_api.webapp.update.assert_called_once_with(
        domain_name=config_dict["webapp"]["default_domain"],
        python_version=Python3.PYTHON310,
        source_directory=f"/home/{username}/foo",
        virtualenv_path=f"/home/{username}/foo_venv",
        force_https=True,
        protection=None,
        protection_username=None,
        protection_password=None,
    )


def test_update_py_src_venv_https_priv(mock_api, config_dict):
    result = runner.invoke(
        app,
        [
            "app", "update",
            "--py", "310",
            "--src", "~/foo",
            "--venv", "~/foo_venv",
            "--https",
            "--priv",
            "-p", "password123",
            "-u", "user321",
        ],
    )  # yapf: disable
    assert result.exit_code == 0, result.stdout

    username = config_dict['api']['username']
    mock_api.webapp.update.assert_called_once_with(
        domain_name=config_dict["webapp"]["default_domain"],
        python_version=Python3.PYTHON310,
        source_directory=f"/home/{username}/foo",
        virtualenv_path=f"/home/{username}/foo_venv",
        force_https=True,
        protection=True,
        protection_username="user321",
        protection_password="password123",
    )


def test_update_http_pub(mock_api, config_dict):
    result = runner.invoke(app, ["app", "update", "--http", "--pub"])
    assert result.exit_code == 0, result.stdout

    mock_api.webapp.update.assert_called_once_with(
        domain_name=config_dict["webapp"]["default_domain"],
        python_version=None,
        source_directory=None,
        virtualenv_path=None,
        force_https=False,
        protection=False,
        protection_username=None,
        protection_password=None,
    )


def test_rm_default(mock_api, config_dict):
    result = runner.invoke(app, ["app", "rm"])
    assert result.exit_code == 0, result.stdout
    mock_api.webapp.delete.assert_called_once_with(
        config_dict["webapp"]["default_domain"]
    )


def test_rm_custom(mock_api):
    result = runner.invoke(app, ["app", "rm", "foobar1.baz"])
    assert result.exit_code == 0, result.stdout
    mock_api.webapp.delete.assert_called_once_with("foobar1.baz")


def test_on_default(mock_api, config_dict):
    result = runner.invoke(app, ["app", "on"])
    assert result.exit_code == 0, result.stdout
    mock_api.webapp.enable.assert_called_once_with(
        config_dict["webapp"]["default_domain"]
    )


def test_off_default(mock_api, config_dict):
    result = runner.invoke(app, ["app", "off"])
    assert result.exit_code == 0, result.stdout
    mock_api.webapp.disable.assert_called_once_with(
        config_dict["webapp"]["default_domain"]
    )


def test_reload_default(mock_api, config_dict):
    result = runner.invoke(app, ["app", "reload"])
    assert result.exit_code == 0, result.stdout
    mock_api.webapp.reload.assert_called_once_with(
        config_dict["webapp"]["default_domain"]
    )


def test_header_ls(mock_api, config_dict):
    result = runner.invoke(app, ["app", "header", "ls"])
    assert result.exit_code == 0, result.stdout
    mock_api.webapp.list_static_headers.assert_called_once_with(
        config_dict["webapp"]["default_domain"]
    )


def test_header_add(mock_api, config_dict):
    result = runner.invoke(
        app,
        [
            "app", "header", "add",
            "-n", "header_name",
            "-v", "header_value",
            "--url", "https://foo.bar",
        ],
    )  # yapf: disable
    assert result.exit_code == 0, result.stdout
    mock_api.webapp.add_static_header.assert_called_once_with(
        domain_name=config_dict["webapp"]["default_domain"],
        name="header_name",
        value="header_value",
        url="https://foo.bar",
    )


def test_header_update(mock_api, config_dict):
    result = runner.invoke(
        app,
        [
            "app", "header", "update", "123456",
            "-n", "header_name",
            "-v", "header_new_value",
            "--url", "https://foo.bar",
        ],
    )  # yapf: disable
    assert result.exit_code == 0, result.stdout
    mock_api.webapp.update_static_header.assert_called_once_with(
        domain_name=config_dict["webapp"]["default_domain"],
        header_id=123456,
        value="header_new_value",
        name="header_name",
        url="https://foo.bar",
    )


def test_header_info(mock_api, config_dict):
    result = runner.invoke(app, ["app", "header", "info", "123456"])
    assert result.exit_code == 0, result.stdout
    mock_api.webapp.get_static_header_info.assert_called_once_with(
        config_dict["webapp"]["default_domain"], 123456
    )


def test_header_rm(mock_api, config_dict):
    result = runner.invoke(app, ["app", "header", "rm", "123456"])
    assert result.exit_code == 0, result.stdout
    mock_api.webapp.delete_static_header.assert_called_once_with(
        config_dict["webapp"]["default_domain"], 123456
    )


def test_ssl_info(mock_api, config_dict):
    result = runner.invoke(app, ["app", "ssl", "info"])
    assert result.exit_code == 0, result.stdout
    mock_api.webapp.get_ssl_info.assert_called_once_with(
        config_dict["webapp"]["default_domain"]
    )


def test_ssl_add_cli(mock_api, config_dict):
    result = runner.invoke(
        app, [
            "app", "ssl", "add",
            "--cert", "cert-value",
            "--key", "key-value",
        ],
    )  # yapf: disable
    assert result.exit_code == 0, result.stdout
    mock_api.webapp.add_ssl.assert_called_once_with(
        domain_name=config_dict["webapp"]["default_domain"],
        cert="cert-value",
        private_key="key-value",
    )


def test_ssl_add_file(mock_api, config_dict, tmp_path):
    cert = tmp_path / "foo.cert"
    cert.write_text("cert-value")

    key = tmp_path / "bar.key"
    key.write_text("key-value")

    result = runner.invoke(
        app, [
            "app", "ssl", "add",
            "--cert", str(cert),
            "--key", str(key),
        ],
    )  # yapf: disable
    assert result.exit_code == 0, result.stdout
    mock_api.webapp.add_ssl.assert_called_once_with(
        domain_name=config_dict["webapp"]["default_domain"],
        cert="cert-value",
        private_key="key-value",
    )


def test_ssl_rm(mock_api, config_dict):
    result = runner.invoke(app, ["app", "ssl", "rm"])
    assert result.exit_code == 0, result.stdout
    mock_api.webapp.delete_ssl.assert_called_once_with(
        config_dict["webapp"]["default_domain"]
    )


def test_static_ls(mock_api, config_dict):
    result = runner.invoke(app, ["app", "static", "ls"])
    assert result.exit_code == 0, result.stdout
    mock_api.webapp.list_static_files.assert_called_once_with(
        config_dict["webapp"]["default_domain"]
    )


def test_static_add(mock_api, config_dict):
    result = runner.invoke(
        app, [
            "app", "static", "add",
            "-u", "static.foo.bar",
            "-p", "/static",
        ],
    )  # yapf: disable
    assert result.exit_code == 0, result.stdout
    mock_api.webapp.add_static_file.assert_called_once_with(
        config_dict["webapp"]["default_domain"],
        "static.foo.bar",
        "/static",
    )


def test_static_info(mock_api, config_dict):
    result = runner.invoke(app, ["app", "static", "info", "123456"])
    assert result.exit_code == 0, result.stdout
    mock_api.webapp.get_static_file_info.assert_called_once_with(
        config_dict["webapp"]["default_domain"], 123456
    )


def test_static_update(mock_api, config_dict, username):
    result = runner.invoke(
        app, [
            "app", "static", "update", "123456",
            "-u", "static1.foo.bar",
            "-p", "~/foo/static",
        ],
    )  # yapf: disable
    assert result.exit_code == 0, result.stdout
    mock_api.webapp.update_static_file.assert_called_once_with(
        domain_name=config_dict["webapp"]["default_domain"],
        url="static1.foo.bar",
        file_id=123456,
        path=f"/home/{username}/foo/static",
    )


def test_static_rm(mock_api, config_dict):
    result = runner.invoke(app, ["app", "static", "rm", "123456"])
    assert result.exit_code == 0, result.stdout
    mock_api.webapp.delete_static_file.assert_called_once_with(
        config_dict["webapp"]["default_domain"], 123456
    )


def test_wsgi_fallback_domain(monkeypatch, mock_api, mock_context_object):
    monkeypatch.setitem(
        mock_context_object.config["webapp"], "default_domain", ""
    )
    with mock.patch(f"{MODULE}.app.cat") as cat:
        result = runner.invoke(app, ["app", "wsgi"])
    assert result.exit_code == 0, result.stdout

    username = mock_context_object.credentials.username
    wsgi = f"/var/www/{username}_pythonanywhere_com_wsgi.py"
    cat.assert_called_once_with(mock.ANY, wsgi)


@pytest.mark.parametrize("log", ("error", "access", "server"))
def test_log_fallback_domain(monkeypatch, mock_api, mock_context_object, log):
    monkeypatch.setitem(
        mock_context_object.config["webapp"], "default_domain", ""
    )
    with mock.patch(f"{MODULE}.app.cat") as cat:
        result = runner.invoke(app, ["app", "log", log])
    assert result.exit_code == 0, result.stdout

    username = mock_context_object.credentials.username
    log_file = f"/var/log/{username}.pythonanywhere.com.{log}.log"
    cat.assert_called_once_with(mock.ANY, log_file)


@pytest.mark.parametrize("log", ("error", "access", "server"))
def test_log_default_domain(monkeypatch, mock_api, mock_context_object, log):
    with mock.patch(f"{MODULE}.app.cat") as cat:
        result = runner.invoke(app, ["app", "log", log])
    assert result.exit_code == 0, result.stdout

    domain = mock_context_object.config["webapp"]["default_domain"]
    log_file = f"/var/log/{domain}.{log}.log"
    cat.assert_called_once_with(mock.ANY, log_file)


def test_wsgi_default_domain(monkeypatch, mock_api, mock_context_object):
    with mock.patch(f"{MODULE}.app.cat") as cat:
        result = runner.invoke(app, ["app", "wsgi"])
    assert result.exit_code == 0, result.stdout

    domain = (
        mock_context_object.config["webapp"]
        ["default_domain"].replace(".", "_")
    )
    wsgi = f"/var/www/{domain}_wsgi.py"
    cat.assert_called_once_with(mock.ANY, wsgi)


def test_wsgi_default_domain_update(monkeypatch, mock_api, mock_context_object):
    with mock.patch(f"{MODULE}.app.upload") as upload:
        with runner.isolated_filesystem():
            new_wsgi = Path("wsgi.py").resolve()
            with new_wsgi.open("w") as f:
                f.write("foo")
            result = runner.invoke(app, ["app", "wsgi", "-u", new_wsgi])

    assert result.exit_code == 0, result.stdout
    domain = (
        mock_context_object.config["webapp"]
        ["default_domain"].replace(".", "_")
    )
    wsgi = f"/var/www/{domain}_wsgi.py"
    upload.assert_called_once_with(mock.ANY, new_wsgi, wsgi)
