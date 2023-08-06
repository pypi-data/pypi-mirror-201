from __future__ import annotations

from typing import Optional

from pawapi import SystemImage
from typer import Context
from typer import Option
from typer import Typer

from pawcli.core.callback import init_api
from pawcli.core.enum import Python3Version
from pawcli.core.enum import PythonVersion
from pawcli.core.result import process_result

PYTHON_VERSION_OPTION = Option(None, "--set", help="Set python version")

system_app = Typer(
    callback=init_api,
    help="Manage system parameters",
)


@system_app.command()
def image(
    ctx: Context,
    version: Optional[SystemImage] = Option(
        None,
        "--set",
        help="Set system image",
    ),
) -> None:
    """System image"""

    api = ctx.obj.api.system
    if version is None:
        result = api.get_current_image()
    else:
        result = api.set_version(version)
    process_result(result)


@system_app.command()
def py(
    ctx: Context,
    version: Optional[PythonVersion] = PYTHON_VERSION_OPTION,
) -> None:
    """Python version"""

    api = ctx.obj.api.python
    if version is None:
        result = api.get_python_version()
    else:
        result = api.set_python_version(version.as_external())
    process_result(result)


@system_app.command()
def py3(
    ctx: Context,
    version: Optional[Python3Version] = PYTHON_VERSION_OPTION,
) -> None:
    """Python 3 version"""

    api = ctx.obj.api.python
    if version is None:
        result = api.get_python3_version()
    else:
        result = api.set_python3_version(version.as_external())
    process_result(result)


@system_app.command()
def sar(
    ctx: Context,
    version: Optional[Python3Version] = PYTHON_VERSION_OPTION,
) -> None:
    """SaveAndRun Python version"""

    api = ctx.obj.api.python
    if version is None:
        result = api.get_sar_version()
    else:
        result = api.set_sar_version(version.as_external())
    process_result(result)


@system_app.command()
def cpu(ctx: Context) -> None:
    """CPU usage information"""

    result = ctx.obj.api.cpu.get_info()
    process_result(result)
