from __future__ import annotations

from typer import Context
from typer import Typer

from pawcli.core.result import process_result

from .params import DOMAIN_ARGUMENT
from .params import DOMAIN_OPTION
from .params import HEADER_ID_ARGUMENT
from .params import HEADER_NAME_OPTION
from .params import HEADER_URL_OPTION
from .params import HEADER_VALUE_OPTION

header_app = Typer(help="Manage static headers")


@header_app.command()
def ls(
    ctx: Context,
    domain: str = DOMAIN_ARGUMENT,
) -> None:
    """List all static headers for app"""

    result = ctx.obj.api.webapp.list_static_headers(domain)
    process_result(result)


@header_app.command(short_help="Create a new statis header")
def add(
    ctx: Context,
    url: str = HEADER_URL_OPTION,
    name: str = HEADER_NAME_OPTION,
    value: str = HEADER_VALUE_OPTION,
    domain: str = DOMAIN_OPTION,
) -> None:
    """Create a new statis header

    App restart required.
    """

    result = ctx.obj.api.webapp.add_static_header(
        domain_name=domain,
        url=url,
        name=name,
        value=value,
    )
    process_result(result, expected_status=201)


@header_app.command()
def info(
    ctx: Context,
    header_id: int = HEADER_ID_ARGUMENT,
    domain: str = DOMAIN_OPTION,
) -> None:
    """App static header details"""

    result = ctx.obj.api.webapp.get_static_header_info(domain, header_id)
    process_result(result)


@header_app.command(short_help="Update app static header")
def update(
    ctx: Context,
    header_id: int = HEADER_ID_ARGUMENT,
    url: str = HEADER_URL_OPTION,
    name: str = HEADER_NAME_OPTION,
    value: str = HEADER_VALUE_OPTION,
    domain: str = DOMAIN_OPTION,
) -> None:
    """Update app static header

    App restart required.
    """

    result = ctx.obj.api.webapp.update_static_header(
        domain_name=domain,
        header_id=header_id,
        url=url,
        name=name,
        value=value,
    )
    process_result(result)


@header_app.command(short_help="Remove app static header")
def rm(
    ctx: Context,
    header_id: int = HEADER_ID_ARGUMENT,
    domain: str = DOMAIN_OPTION,
) -> None:
    """Remove app static header

    App restart required.
    """

    result = ctx.obj.api.webapp.delete_static_header(domain, header_id)
    process_result(result, expected_status=204, print_content=False)
