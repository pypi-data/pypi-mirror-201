from __future__ import annotations

from typer import Context
from typer import Typer

from pawcli.core.result import process_result

from .params import DOMAIN_ARGUMENT
from .params import DOMAIN_OPTION
from .params import FILE_ID_ARGUMENT
from .params import FILES_PATH_OPTION
from .params import FILES_URL_OPTION

static_app = Typer(help="Manage static files")


@static_app.command()
def ls(
    ctx: Context,
    domain: str = DOMAIN_ARGUMENT,
) -> None:
    """List static files"""

    result = ctx.obj.api.webapp.list_static_files(domain)
    process_result(result)


@static_app.command(short_help="Add static files")
def add(
    ctx: Context,
    domain: str = DOMAIN_ARGUMENT,
    url: str = FILES_URL_OPTION,
    path: str = FILES_PATH_OPTION,
) -> None:
    """Add static files

    App restart required.
    """

    result = ctx.obj.api.webapp.add_static_file(domain, url, path)
    process_result(result, expected_status=201)


@static_app.command()
def info(
    ctx: Context,
    file_id: int = FILE_ID_ARGUMENT,
    domain: str = DOMAIN_OPTION,
) -> None:
    """Static files details"""

    resutl = ctx.obj.api.webapp.get_static_file_info(domain, file_id)
    process_result(resutl)


@static_app.command(short_help="Update static file")
def update(
    ctx: Context,
    file_id: int = FILE_ID_ARGUMENT,
    url: str = FILES_URL_OPTION,
    path: str = FILES_PATH_OPTION,
    domain: str = DOMAIN_OPTION,
) -> None:
    """Update static file

    App restart required.
    """

    result = ctx.obj.api.webapp.update_static_file(
        domain_name=domain,
        file_id=file_id,
        url=url,
        path=path,
    )
    process_result(result)


@static_app.command(short_help="Remove static file")
def rm(
    ctx: Context,
    file_id: int = FILE_ID_ARGUMENT,
    domain: str = DOMAIN_OPTION,
) -> None:
    """Remove static file

    App restart required.
    """

    resutl = ctx.obj.api.webapp.delete_static_file(domain, file_id)
    process_result(resutl, expected_status=204, print_content=False)
