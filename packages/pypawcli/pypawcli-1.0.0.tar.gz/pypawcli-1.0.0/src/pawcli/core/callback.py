from __future__ import annotations

from configparser import Error as ConfigError
from pathlib import Path
from typing import Optional

from pawapi import Pawapi
from pawapi import Region
from pawapi.exceptions import InvalidCredentialsError
from typer import Context
from typer import Exit
from typer import Option
from typer import prompt

from pawcli.version import __version__

from .config import APP_NAME
from .config import Config
from .context import ContextObject
from .context import Credentials


def init_api(ctx: Context) -> None:
    timeout = ctx.parent.params.get("timeout", None)
    if timeout is None:
        try:
            timeout = ctx.obj.config.getfloat("api", "timeout")
        except ValueError as error:
            print(f"api.timeout (config file): {error}")
            ctx.exit(1)
    try:
        ctx.obj.api = Pawapi(
            token=ctx.obj.credentials.token,
            username=ctx.obj.credentials.username,
            region=ctx.obj.credentials.region,
            timeout=timeout,
        )
    except InvalidCredentialsError as error:
        print(error)
        ctx.exit(1)


def __show_version(version: bool) -> None:  # pragma: no cover
    if version:
        print(f"{APP_NAME} {__version__}")
        raise Exit()


def init_context_object(
    ctx: Context,
    username: Optional[str] = Option(
        None,
        "--username",
        "-u",
        envvar="PAWCLI_USERNAME",
        metavar="USERNAME",
        help="PythonAnywhere Username",
    ),
    token: Optional[str] = Option(
        None,
        "--token",
        "-t",
        envvar="PAWCLI_TOKEN",
        metavar="TOKEN",
        help="API Token",
    ),
    region: Optional[Region] = Option(
        None,
        "--region",
        "-r",
        envvar="PAWCLI_REGION",
        help="Account Region",
    ),
    config_file: Optional[Path] = Option(
        None,
        "--config",
        "-c",
        envvar="PAWCLI_CONFIG",
        metavar="PATH",
        exists=True,
        help="Custom path to config",
    ),
    timeout: Optional[float] = Option(
        None,
        "--timeout",
        "-T",
        metavar="SEC",
        min=0,
        help="Request timeout",
    ),
    version: bool = Option(
        False,
        "--version",
        "-v",
        is_eager=True,
        is_flag=True,
        callback=__show_version,
        help="Output version information and exit",
    ),
) -> None:
    try:
        config = Config(config=config_file)
    except (ConfigError, IOError) as error:  # pragma: no cover
        print(f"Can't init config: {error}")
        ctx.exit(1)

    if token == "--":  # pragma: no cover
        token = prompt("Token", hide_input=True, type=str)

    username = username or config.get("api", "username", fallback=None)
    token = token or config.get("api", "token", fallback=None)

    try:
        region = region or Region(config.get("api", "region"))
    except ValueError as error:  # pragma: no cover
        print(f"api.region (config file): {error}")
        ctx.exit(1)

    ctx.obj = ContextObject(
        config=config,
        credentials=Credentials(
            username=username,
            token=token,
            region=region,
        ),
    )
