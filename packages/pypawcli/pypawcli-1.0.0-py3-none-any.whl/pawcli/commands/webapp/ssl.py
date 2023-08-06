from __future__ import annotations

from pathlib import Path

from typer import Context
from typer import Option
from typer import Typer

from pawcli.core.result import process_result

from .params import DOMAIN_ARGUMENT

ssl_app = Typer(help="Manage app certificate")


@ssl_app.command()
def info(
    ctx: Context,
    domain: str = DOMAIN_ARGUMENT,
) -> None:
    """Certificate details"""

    result = ctx.obj.api.webapp.get_ssl_info(domain)
    process_result(result)


@ssl_app.command(short_help="Add a new certificate")
def add(
    ctx: Context,
    domain: str = DOMAIN_ARGUMENT,
    cert: str = Option(
        ...,
        "--cert",
        metavar="TEXT | PATH",
        help="Certificate",
    ),
    key: str = Option(
        ...,
        "--key",
        metavar="TEXT | PATH",
        help="Private key",
    ),
) -> None:
    """Add a new certificate

    Certificate/Key can be plain text or path to file with .cert/.key extension.
    """

    def _read(f: str) -> str:  # pragma: no cover
        p = Path(f).expanduser().resolve()
        if not p.exists():
            ctx.fail(f"{p} does not exist")
        try:
            return p.read_text()
        except IOError:
            print(f"Can't read {p}")
            ctx.exit(1)

    if cert.endswith(".cert"):
        cert = _read(cert)
    if key.endswith(".key"):
        key = _read(key)

    result = ctx.obj.api.webapp.add_ssl(
        domain_name=domain,
        cert=cert,
        private_key=key,
    )
    process_result(result, expected_status=201)


@ssl_app.command()
def rm(
    ctx: Context,
    domain: str = DOMAIN_ARGUMENT,
) -> None:
    """Remove certificate"""

    result = ctx.obj.api.webapp.delete_ssl(domain)
    process_result(result, expected_status=204, print_content=False)
