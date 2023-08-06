from typer import Argument
from typer import Option

COMMAND_ARGUMENT = Argument(
    ...,
    metavar="CMD",
    help="Command to execute",
)
COMMAND_OPTION = Option(
    None,
    "--command",
    "-c",
    metavar="CMD",
    help="Command to execute",
)
TASK_ID_ARGUMENT = Argument(
    ...,
    metavar="ID",
    help="Task ID",
)
MINUTE_OPTION = Option(
    None,
    "--minute",
    "-M",
    metavar="NUM",
    min=0,
    max=59,
    help="Start at",
)
HOUR_OPTION = Option(
    None,
    "--hour",
    "-H",
    min=0,
    max=23,
    metavar="NUM",
    help="Start at",
)
DESCRIPTION_OPTION = Option(
    None,
    "--description",
    "-d",
    metavar="TEXT",
    help="Task description",
)
ENABLED_OPTION = Option(
    None,
    "--enable/--disable",
    is_flag=True,
    help="Enable/disable task",
)
INTERVAL_OPTION = Option(
    None,
    "--interval",
    "-i",
    help="Start interval",
)
