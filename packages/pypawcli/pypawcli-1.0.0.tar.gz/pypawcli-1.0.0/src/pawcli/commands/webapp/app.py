from __future__ import annotations

from pathlib import Path
from typing import Optional

from typer import Context
from typer import Option
from typer import Typer

from pawcli.commands.file import cat
from pawcli.commands.file import upload
from pawcli.core.callback import init_api
from pawcli.core.enum import AppLog
from pawcli.core.enum import Python3Version
from pawcli.core.path import resolve
from pawcli.core.result import process_result
from pawcli.core.utils import save_config

from .params import DOMAIN_ARGUMENT
from .params import DOMAIN_OPTION
from .params import PYTHON_VERSION_OPTION

webapp_app = Typer(help="Manage webapps")


@webapp_app.callback()
def _setup_context(ctx: Context) -> None:  # pragma: no cover
    init_api(ctx)

    default_domain = ctx.obj.config.get(
        "webapp", "default_domain", fallback=None
    )
    if default_domain is None or not default_domain:
        username = ctx.obj.credentials.username
        default_domain = f"{username}.pythonanywhere.com"

    ctx.default_map = {
        "new": {
            "python": ctx.obj.config.get("webapp", "python"),
            "domain": default_domain,
        },
        "update": {"domain": default_domain},
        "info": {"domain": default_domain},
        "on": {"domain": default_domain},
        "off": {"domain": default_domain},
        "rm": {"domain": default_domain},
        "reload": {"domain": default_domain},
        "wsgi": {"domain": default_domain},
        "log": {"domain": default_domain},
        "header": {
            "ls": {"domain": default_domain},
            "add": {"domain": default_domain},
            "info": {"domain": default_domain},
            "update": {"domain": default_domain},
            "rm": {"domain": default_domain},
        },
        "ssl": {
            "info": {"domain": default_domain},
            "add": {"domain": default_domain},
            "rm": {"domain": default_domain},
        },
        "static": {
            "ls": {"domain": default_domain},
            "add": {"domain": default_domain},
            "info": {"domain": default_domain},
            "update": {"domain": default_domain},
            "rm": {"domain": default_domain},
        },
    }  # yapf: disable


@webapp_app.command()
def ls(ctx: Context):
    """List all webapps"""

    result = ctx.obj.api.webapp.list()
    process_result(result)


@webapp_app.command()
def info(
    ctx: Context,
    domain: str = DOMAIN_ARGUMENT,
) -> None:
    """App configuration"""

    result = ctx.obj.api.webapp.get_info(domain)
    process_result(result)


@webapp_app.command(short_help="Create a new app")
def new(
    ctx: Context,
    domain: str = DOMAIN_ARGUMENT,
    python: Optional[Python3Version] = PYTHON_VERSION_OPTION,
    default: bool = Option(
        False,
        "--default",
        "-D",
        is_flag=True,
        help="Use app as default for `domain` argument",
    ),
) -> None:
    """ \b
    Create a new app with minimal configuration.
    Use `update` command to setup your app.
    """

    if default:
        ctx.obj.config.set("webapp", "default_domain", domain)
        save_config(ctx)

    result = ctx.obj.api.webapp.create(domain, python.as_external())
    process_result(result)


@webapp_app.command(short_help="Modify configuration")
def update(
    ctx: Context,
    domain: str = DOMAIN_ARGUMENT,
    python: Optional[Python3Version] = PYTHON_VERSION_OPTION,
    src: Optional[str] = Option(
        None,
        metavar="PATH",
        help="Source directory",
    ),
    venv: Optional[str] = Option(
        None,
        metavar="PATH",
        help="Virtualenv path",
    ),
    https: Optional[bool] = Option(
        None,
        "--https/--http",
        is_flag=True,
        help="Enbale/Disable force HTTPS",
    ),
    protection: Optional[bool] = Option(
        None,
        "--priv/--pub",
        is_flag=True,
        help="Enable/Disable password protection",
    ),
    username: Optional[str] = Option(
        None,
        "--username",
        "-u",
        help="Username for password protection",
    ),
    password: Optional[str] = Option(
        None,
        "--password",
        "-p",
        help="Password for password protection",
    ),
) -> None:
    """Modify configuration

    App restart required.
    """

    result = ctx.obj.api.webapp.update(
        domain_name=domain,
        python_version=python.as_external() if python is not None else None,
        source_directory=resolve(ctx, src) if src is not None else None,
        virtualenv_path=resolve(ctx, venv) if venv is not None else None,
        force_https=https,
        protection=protection,
        protection_username=username,
        protection_password=password,
    )
    process_result(result, expected_status=[201, 200])


@webapp_app.command(short_help="Delete the app")
def rm(
    ctx: Context,
    domain: str = DOMAIN_ARGUMENT,
) -> None:
    """Delete the app

    WSGI config and your code is not touched.
    """

    result = ctx.obj.api.webapp.delete(domain)
    process_result(result, expected_status=204)


@webapp_app.command()
def on(
    ctx: Context,
    domain: str = DOMAIN_ARGUMENT,
) -> None:
    """Enable the app"""

    result = ctx.obj.api.webapp.enable(domain)
    process_result(result)


@webapp_app.command()
def off(
    ctx: Context,
    domain: str = DOMAIN_ARGUMENT,
) -> None:
    """Disable the app"""

    result = ctx.obj.api.webapp.disable(domain)
    process_result(result)


@webapp_app.command()
def reload(
    ctx: Context,
    domain: str = DOMAIN_ARGUMENT,
) -> None:
    """Reload the app"""

    result = ctx.obj.api.webapp.reload(domain)
    process_result(result)


@webapp_app.command()
def log(
    ctx: Context,
    log: AppLog,
    domain: str = DOMAIN_OPTION,
) -> None:
    """App log"""

    cat(ctx, f"/var/log/{domain}.{log.value}.log")


@webapp_app.command(short_help="WSGI config")
def wsgi(
    ctx: Context,
    domain: str = DOMAIN_ARGUMENT,
    update: Optional[Path] = Option(
        None,
        "--update",
        "-u",
        exists=True,
        help="Upload a new wsgi config",
    ),
) -> None:
    """Get WSGI config file or upload a new one

    App restart required to apply new config.
    """

    wsgi_config_path = f"/var/www/{domain.replace('.', '_')}_wsgi.py"
    if update is None:
        cat(ctx, wsgi_config_path)
    else:
        upload(ctx, update, wsgi_config_path)
