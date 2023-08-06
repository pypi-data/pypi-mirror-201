from __future__ import annotations

from configparser import NoOptionError
from configparser import NoSectionError
from typing import Optional

from typer import Argument
from typer import BadParameter
from typer import Context
from typer import Option
from typer import Typer

from .commands import console_app
from .commands import file_app
from .commands import scheduled_app
from .commands import students_app
from .commands import system_app
from .commands import webapp_app
from .core.callback import init_context_object
from .core.utils import save_config

app = Typer(
    add_completion=False,
    callback=init_context_object,
    context_settings={
        "help_option_names": ("-h", "--help"),
        "max_content_width": 88,
    },
    help="CLI tool for PythonAnywhere",
)

app.add_typer(console_app, name="console")
app.add_typer(file_app, name="file")
app.add_typer(students_app, name="students")
app.add_typer(system_app, name="sys")
app.add_typer(scheduled_app, name="task")
app.add_typer(webapp_app, name="app")


@app.command()
def config(
    ctx: Context,
    parameter: str = Argument(
        ...,
        help="Config option",
        metavar="OPTION",
    ),
    value: Optional[str] = Option(
        None,
        "--set",
        metavar="VALUE",
        help="Set new value",
    ),
    delete: Optional[bool] = Option(
        False,
        "--del",
        is_flag=True,
        help="Reset value",
    ),
) -> None:
    """Manage local config"""

    sect_opt = parameter.split(".", maxsplit=1)
    if len(sect_opt) != 2:  # pragma: no cover
        raise BadParameter(parameter)

    cfg = ctx.obj.config
    result = value
    try:
        if delete:
            if cfg.remove_option(*sect_opt):  # pragma: no cover
                save_config(ctx)
        elif value is not None:
            cfg.set(*sect_opt, value)
            save_config(ctx)
        else:
            try:
                result = cfg.get(*sect_opt)
            except NoOptionError:
                pass
    except NoSectionError as error:
        print(error)
        ctx.exit(1)

    print(f"{parameter} = {result or '<undefined>'}")
