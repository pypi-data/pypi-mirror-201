from __future__ import annotations

from typing import Optional

from typer import Context
from typer import Typer

from pawcli.commands.file import cat
from pawcli.core.result import process_result

from .params import COMMAND_ARGUMENT
from .params import COMMAND_OPTION
from .params import DESCRIPTION_OPTION
from .params import ENABLED_OPTION
from .params import TASK_ID_ARGUMENT

alwayson_app = Typer(help="Manage Always-on tasks")


@alwayson_app.command()
def ls(ctx: Context) -> None:
    """List all tasks"""

    result = ctx.obj.api.alwayson_task.list()
    process_result(result)


@alwayson_app.command()
def new(
    ctx: Context,
    command: str = COMMAND_ARGUMENT,
    enabled: Optional[bool] = ENABLED_OPTION,
    description: Optional[str] = DESCRIPTION_OPTION,
) -> None:
    """Create a new task"""

    result = ctx.obj.api.alwayson_task.create(
        command=command,
        enabled=enabled,
        description=description,
    )
    process_result(result, expected_status=201)


@alwayson_app.command()
def update(
    ctx: Context,
    task_id: int = TASK_ID_ARGUMENT,
    enabled: Optional[bool] = ENABLED_OPTION,
    description: Optional[str] = DESCRIPTION_OPTION,
    command: Optional[str] = COMMAND_OPTION,
) -> None:
    """Modify task"""

    result = ctx.obj.api.alwayson_task.update(
        task_id=task_id,
        command=command,
        description=description,
        enabled=enabled,
    )
    process_result(result)


@alwayson_app.command()
def info(ctx: Context, task_id: int = TASK_ID_ARGUMENT) -> None:
    """Task information"""

    result = ctx.obj.api.alwayson_task.get_info(task_id)
    process_result(result)


@alwayson_app.command()
def rm(ctx: Context, task_id: int = TASK_ID_ARGUMENT) -> None:
    """Delete the task"""

    result = ctx.obj.api.alwayson_task.delete(task_id)
    process_result(result, expected_status=204, print_content=False)


@alwayson_app.command()
def log(ctx: Context, task_id: int = TASK_ID_ARGUMENT) -> None:
    """Task log"""

    cat(ctx, f"/var/log/alwayson-log-{task_id}.log")
