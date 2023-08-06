from __future__ import annotations

from typer import Argument
from typer import Context
from typer import Typer

from pawcli.core.callback import init_api
from pawcli.core.result import process_result

students_app = Typer(
    callback=init_api,
    help="Manage students",
)


@students_app.command()
def ls(ctx: Context) -> None:
    """List of students"""

    result = ctx.obj.api.students.list()
    process_result(result)


@students_app.command()
def rm(ctx: Context, id_: str = Argument(..., metavar="ID")) -> None:
    """Remove the student"""

    result = ctx.obj.api.students.delete(id_)
    process_result(result, expected_status=204, print_content=False)
