from __future__ import annotations

from typing import Optional

from pawapi import TaskInterval
from typer import Context
from typer import Typer

from pawcli.commands.file import cat
from pawcli.core.callback import init_api
from pawcli.core.result import process_result

from .params import COMMAND_ARGUMENT
from .params import COMMAND_OPTION
from .params import DESCRIPTION_OPTION
from .params import ENABLED_OPTION
from .params import HOUR_OPTION
from .params import INTERVAL_OPTION
from .params import MINUTE_OPTION
from .params import TASK_ID_ARGUMENT

scheduled_app = Typer(help="Manage tasks")


@scheduled_app.callback()
def _setup_context(ctx: Context):
    init_api(ctx)
    ctx.default_map = {
        "new": {
            "minute": 0,
            "hour": 0,
            "interval": "daily",
        },
    }


@scheduled_app.command()
def ls(ctx: Context) -> None:
    """List all tasks"""

    result = ctx.obj.api.scheduled_task.list()
    process_result(result)


@scheduled_app.command()
def new(
    ctx: Context,
    command: str = COMMAND_ARGUMENT,
    minute: Optional[int] = MINUTE_OPTION,
    hour: Optional[int] = HOUR_OPTION,
    enabled: Optional[bool] = ENABLED_OPTION,
    interval: Optional[TaskInterval] = INTERVAL_OPTION,
    description: Optional[str] = DESCRIPTION_OPTION,
) -> None:
    """Create a new task"""

    result = ctx.obj.api.scheduled_task.create(
        command=command,
        minute=minute,
        hour=hour,
        enabled=enabled,
        interval=interval,
        description=description,
    )
    process_result(result, expected_status=201)


@scheduled_app.command()
def update(
    ctx: Context,
    task_id: int = TASK_ID_ARGUMENT,
    command: Optional[str] = COMMAND_OPTION,
    minute: Optional[int] = MINUTE_OPTION,
    hour: Optional[int] = HOUR_OPTION,
    enabled: Optional[bool] = ENABLED_OPTION,
    interval: Optional[TaskInterval] = INTERVAL_OPTION,
    description: Optional[str] = DESCRIPTION_OPTION,
) -> None:
    """Modify task"""

    result = ctx.obj.api.scheduled_task.update(
        task_id=task_id,
        command=command,
        minute=minute,
        hour=hour,
        enabled=enabled,
        interval=interval,
        description=description,
    )
    process_result(result)


@scheduled_app.command()
def info(ctx: Context, task_id: int = TASK_ID_ARGUMENT) -> None:
    """Task information"""

    result = ctx.obj.api.scheduled_task.get_info(task_id)
    process_result(result)


@scheduled_app.command()
def rm(ctx: Context, task_id: int = TASK_ID_ARGUMENT) -> None:
    """Delete the task"""

    result = ctx.obj.api.scheduled_task.delete(task_id)
    process_result(result, expected_status=204, print_content=False)


@scheduled_app.command()
def log(ctx: Context, task_id: int = TASK_ID_ARGUMENT) -> None:
    """Task log"""

    cat(ctx, f"/var/log/schedule-log-{task_id}.log")
