import unittest.mock as mock
from pathlib import Path

import pytest
from typer.testing import CliRunner

from pawcli.app import app

MODULE = "pawcli.commands.file"

_path = (
    ("~/foo", "/home/{}/foo"),
    ("pa:~foo", "/home/{}/foo"),
    ("/tmp", "/tmp"),
    ("/tmp/bar.py", "/tmp/bar.py"),
)

runner = CliRunner()


@pytest.fixture(autouse=True)
def mock_process_result(monkeypatch, dummy):
    monkeypatch.setattr(f"{MODULE}.process_result", dummy)


@pytest.fixture(autouse=True)
def mock_file_api(monkeypatch):
    monkeypatch.setattr("pawcli.app.file_app.info.callback", None)


@pytest.mark.parametrize(
    "src,esrc,dest",
    (
        ("~/foo.bar", "/home/{}/foo.bar", ""),
        ("pa:~/foo/bar.py", "/home/{}/foo/bar.py", "/tmp/bar.py"),
        ("pa:~/foo/bar.py", "/home/{}/foo/bar.py", "~/bar.py"),
    )
)
@mock.patch(f"{MODULE}.isinstance", new=mock.Mock(return_value=True))
def test_download(mock_api, username, src, esrc, dest):
    with runner.isolated_filesystem():
        with mock.patch("pathlib.Path.write_bytes"):
            result = runner.invoke(app, ["file", "download", src, dest])

    assert result.exit_code == 0, result.stdout
    mock_api.file.get_content.assert_called_once_with(esrc.format(username))


@mock.patch(f"{MODULE}.isinstance", new=mock.Mock(return_value=True))
def test_download_exists(mock_api):
    with runner.isolated_filesystem():
        dest = Path.cwd() / "foo"
        dest.write_text("bar")
        with mock.patch("pathlib.Path.write_bytes"):
            result = runner.invoke(
                app, ["file", "download", "~/bar", str(dest)]
            )

    assert result.exit_code != 0
    mock_api.file.get_content.assert_not_called()
    assert "path exist" in result.stdout


@mock.patch(f"{MODULE}.isinstance", new=mock.Mock(return_value=True))
def test_download_exists_force(mock_api, username):
    with runner.isolated_filesystem():
        dest = Path.cwd() / "foo"
        dest.write_text("bar")
        with mock.patch("pathlib.Path.write_bytes"):
            result = runner.invoke(
                app, ["file", "download", "~/bar", str(dest), "-f"]
            )

    assert result.exit_code == 0, result.stdout
    mock_api.file.get_content.assert_called_once_with(f"/home/{username}/bar")


@mock.patch(f"{MODULE}.isinstance", new=mock.Mock(return_value=False))
def test_download_not_a_file(monkeypatch, mock_api, username):
    with runner.isolated_filesystem():
        dest = Path.cwd() / "foo"
        with mock.patch("pathlib.Path.write_bytes"):
            result = runner.invoke(
                app, ["file", "download", "~/bar", str(dest)]
            )

    assert result.exit_code != 0
    mock_api.file.get_content.assert_called_once_with(f"/home/{username}/bar")
    assert "not a file" in result.stdout


@pytest.mark.parametrize(
    "src,dest,edest",
    (
        (".foo.py", "pa:~/foo.py", "/home/{}/foo.py"),
        ("./bar.py", "pa:~/foo/bar.py", "/home/{}/foo/bar.py"),
    )
)
def test_upload(mock_api, src, dest, edest, username):
    with runner.isolated_filesystem():
        Path(src).expanduser().resolve().write_text("baz")
        result = runner.invoke(app, ["file", "upload", src, dest])

    assert result.exit_code == 0, result.stdout
    mock_api.file.upload.assert_called_once_with(edest.format(username), b"baz")


@mock.patch(f"{MODULE}.isinstance", new=mock.Mock(return_value=True))
def test_cp_download_dest_empty(mock_api, username):
    with runner.isolated_filesystem():
        with mock.patch("pathlib.Path.write_bytes"):
            result = runner.invoke(app, ["file", "cp", "~/foo.bar"])

    assert result.exit_code == 0, result.stdout
    mock_api.file.get_content.assert_called_once_with(
        f"/home/{username}/foo.bar"
    )


@pytest.mark.parametrize(
    "src,esrc,dest",
    (
        ("pa:~/foo/bar.py", "/home/{}/foo/bar.py", "/tmp/bar.py"),
        ("pa:~/foo/bar.py", "/home/{}/foo/bar.py", "~/bar.py"),
    )
)
@mock.patch(f"{MODULE}.isinstance", new=mock.Mock(return_value=True))
def test_cp_download(mock_api, username, src, esrc, dest):
    with runner.isolated_filesystem():
        with mock.patch("pathlib.Path.write_bytes"):
            result = runner.invoke(app, ["file", "cp", src, dest])

    assert result.exit_code == 0, result.stdout
    mock_api.file.get_content.assert_called_once_with(esrc.format(username))


@pytest.mark.parametrize(
    "src,esrc,dest,edest",
    (
        (
            "./foo.py",
            "./foo.py",
            "pa:~/foo.py",
            "/home/{}/foo.py",
        ),
        (
            ".bar.py",
            ".bar.py",
            "pa:~/foo/bar.py",
            "/home/{}/foo/bar.py",
        ),
    )
)
def test_cp_upload(mock_api, src, esrc, dest, edest, username):
    with runner.isolated_filesystem():
        Path(esrc).expanduser().resolve().write_text("foo")
        result = runner.invoke(app, ["file", "cp", src, dest])

    assert result.exit_code == 0, result.stdout
    mock_api.file.upload.assert_called_once_with(edest.format(username), b"foo")


@pytest.mark.parametrize(
    "src,dest", (
        (".foo.py", "pa:~/foo.py"),
        (".bar.py", "pa:~/foo/bar.py"),
    )
)
def test_cp_upload_not_exist(mock_api, src, dest, username):
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["file", "cp", src, dest])

    assert result.exit_code != 0, result.stdout
    mock_api.file.upload.assert_not_called()
    assert "not exist" in result.stdout


@pytest.mark.parametrize(
    "src,dest", (
        (".file.py", "~/file.py"),
        ("pa:~/.file.py", "pa:~/dir/file.py"),
    )
)
def test_cp_both_local_or_remote(src, dest):
    result = runner.invoke(app, ["file", "cp", src, dest])
    assert result.exit_code != 0
    assert "Error" in result.stdout


@pytest.mark.parametrize("in_,out", _path)
def test_rm(mock_api, username, in_, out):
    result = runner.invoke(app, ["file", "rm", in_])
    assert result.exit_code == 0, result.stdout
    mock_api.file.delete.assert_called_once_with(out.format(username))


@pytest.mark.parametrize("in_,out", _path)
def test_cat(mock_api, username, in_, out):
    result = runner.invoke(app, ["file", "cat", in_])
    assert result.exit_code == 0, result.stdout
    mock_api.file.get_content.assert_called_once_with(out.format(username))


@pytest.mark.parametrize("in_,out", _path)
def test_ls(mock_api, username, in_, out):
    result = runner.invoke(app, ["file", "ls", in_])
    assert result.exit_code == 0, result.stdout
    mock_api.file.get_content.assert_called_once_with(out.format(username))


@pytest.mark.parametrize("in_,out", _path)
def test_share_info(mock_api, username, in_, out):
    result = runner.invoke(app, ["file", "share", in_])
    assert result.exit_code == 0, result.stdout
    mock_api.file.get_sharing_status.assert_called_once_with(
        out.format(username)
    )


@pytest.mark.parametrize("in_,out", _path)
def test_share_start(mock_api, username, in_, out):
    result = runner.invoke(app, ["file", "share", in_, "--start"])
    assert result.exit_code == 0, result.stdout
    mock_api.file.start_sharing.assert_called_once_with(out.format(username))


@pytest.mark.parametrize("in_,out", _path)
def test_share_stop(mock_api, username, in_, out):
    result = runner.invoke(app, ["file", "share", in_, "--stop"])
    assert result.exit_code == 0, result.stdout
    mock_api.file.stop_sharing.assert_called_once_with(out.format(username))


@pytest.mark.parametrize("in_,out", _path)
def test_tree(mock_api, username, in_, out):
    result = runner.invoke(app, ["file", "tree", in_])
    assert result.exit_code == 0, result.stdout
    mock_api.file.get_tree.assert_called_once_with(out.format(username))
