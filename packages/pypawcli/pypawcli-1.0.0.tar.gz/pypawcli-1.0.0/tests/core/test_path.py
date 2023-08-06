from pathlib import Path

import pytest

from pawcli.core.path import get_local_output_path
from pawcli.core.path import get_remote_output_path
from pawcli.core.path import resolve


@pytest.mark.parametrize(
    "path,result",
    (
        ("foo", "/foo"),
        ("~file.txt", "/home/{}/file.txt"),
        ("~/.profile", "/home/{}/.profile"),
        ("pa:~/.profile", "/home/{}/.profile"),
        ("tmp/file.txt", "/tmp/file.txt"),
        ("~.tmp/file.txt", "/home/{}/.tmp/file.txt"),
        ("pa:~.tmp/file.txt", "/home/{}/.tmp/file.txt"),
        ("/home/localuser/.profile", "/home/{}/.profile"),
        ("/home/localuser/.local/bin/exec.sh", "/home/{}/.local/bin/exec.sh"),
        ("/home/{}/.profile", "/home/{}/.profile"),
        ("pa:/home/{}/.profile", "/home/{}/.profile"),
        ("home/foo/.profile", "/home/{}/.profile"),
        ("pa:home/foo/.profile", "/home/{}/.profile"),
        ("/user/{}/files/var/www/file", "/var/www/file"),
        ("user/{}/files/var/www/file", "/var/www/file"),
    )
)
def test_resolve(mock_context, username, path, result):
    dest = resolve(mock_context, path.format(username))
    assert dest == result.format(username)


@pytest.mark.parametrize(
    "src,dest,expect",
    (
        ("/foo.py", "{}/foo.py", "{}/foo.py"),
        ("/bar/foo.py", "{}/foo.py", "{}/foo.py"),
        ("/bar/foo.py", "{}/bar.py", "{}/bar.py"),
    )
)
def test_get_local_output_path_file_exist(tmp_path, src, dest, expect):
    f = Path(dest.format(tmp_path))
    f.write_text("foobar")

    result = get_local_output_path(src, str(f), False)
    assert result is None


@pytest.mark.parametrize(
    "src,dest,expect",
    (
        ("/foo.py", "{}/foo.py", "{}/foo.py"),
        ("/bar/foo.py", "{}/foo.py", "{}/foo.py"),
        ("/bar/foo.py", "{}/bar.py", "{}/bar.py"),
    )
)
def test_get_local_output_path_file_exist_force(tmp_path, src, dest, expect):
    f = Path(dest.format(tmp_path))
    f.write_text("foobar")

    result = get_local_output_path(src, str(f), True)
    assert str(result) == expect.format(tmp_path)


@pytest.mark.parametrize(
    "src,dest,expect",
    (
        ("/foo.py", "{}/bar", "{}/bar/foo.py"),
        ("/foobar.py", "{}/foo/bar", "{}/foo/bar/foobar.py"),
    )
)
def test_get_local_output_path_dir_exist(tmp_path, src, dest, expect):
    d = Path(dest.format(tmp_path))
    d.mkdir(parents=True)

    result = get_local_output_path(src, dest.format(tmp_path), False)
    assert str(result) == expect.format(tmp_path)


@pytest.mark.parametrize(
    "in_,out,expect", (
        ("/home/user123/foo", "/home/{}/data/foo", "/home/{}/data/foo"),
        ("/home/user123/data/bar", "/home/{}/", "/home/{}/bar"),
        ("/data/foo", "/home/{}/foobar", "/home/{}/foobar"),
    )
)  # yapf: disable
def test_get_remote_output_path(in_, out, expect, username):
    path = get_remote_output_path(in_, out.format(username))
    assert path == expect.format(username)
