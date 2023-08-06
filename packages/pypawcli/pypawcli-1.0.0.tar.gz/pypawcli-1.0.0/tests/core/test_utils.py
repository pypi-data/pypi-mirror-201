import os

import pytest
from typer import Exit

from pawcli.core.utils import save_config


@pytest.fixture
def config_file(tmp_app_dir):
    file = tmp_app_dir / "config.ini"
    if file.exists():
        file.unlink()
    return file


def test_save_config(mock_context, config_file):
    assert mock_context.obj.config.file == config_file
    save_config(mock_context)
    assert config_file.exists()


def test_save_io_error(mock_context, config_file):
    assert mock_context.obj.config.file == config_file
    if not config_file.exists():
        config_file.write_text("foo")
    os.chmod(config_file, 0o00000)
    save_config(mock_context)
    mock_context.exit.assert_called()


def test_save_io_error_dir(mock_context, config_file):
    mock_context.obj.config.file = config_file.parent / "new_dir" / "config.ini"
    mock_context.exit.side_effect = Exit
    os.chmod(config_file.parent, 0o00000)
    with pytest.raises(Exit):
        save_config(mock_context)
    os.chmod(config_file.parent, 0o0700)


def test_save_new_dir(mock_context, config_file):
    mock_context.obj.config.file = config_file.parent / "new_dir" / "config.ini"
    save_config(mock_context)
    assert mock_context.obj.config.file.exists()
