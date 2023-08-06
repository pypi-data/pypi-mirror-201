from __future__ import annotations

from pathlib import Path
from typing import Optional

from typer import Argument
from typer import Context
from typer import Option
from typer import Typer

from pawcli.core.callback import init_api
from pawcli.core.formatter import ContentFormatter
from pawcli.core.formatter import DirectoryFormatter
from pawcli.core.path import get_local_output_path
from pawcli.core.path import get_remote_output_path
from pawcli.core.path import resolve
from pawcli.core.result import process_result

PATH_REMOTE_ARGUMENT = Argument(
    ...,
    metavar="PATH",
    callback=resolve,
    help="Remote path",
)

PATH_LOCAL_ARGUMENT = Argument(
    ...,
    metavar="PATH",
    help="Local path",
)

file_app = Typer(
    callback=init_api,
    help="Manage files and directories",
)


@file_app.command(short_help="Copy file")
def cp(
    ctx: Context,
    source: str = Argument(...),
    dest: Optional[str] = Argument(None),
    force: bool = Option(
        False,
        "--force",
        "-f",
        is_flag=True,
        help="Ignore existing file (only local dest)",
    ),
) -> None:
    """Copy source to dest.

    Shortcut for upload/download.
    Remote path must begin with prefix (default `pa:`) if dest
    is provided. By default dest is cwd and source is remote path.

    \b
    Example:
    $ cp ~/foo                   # download (dest is cwd)
    $ cp ~/foo pa:~/foo          # upload
    $ cp pa:/foo/bar ~/foo/bar   # download
    $ cp ~/foo ~/bar             # error
    $ cp pa:~/foo pa:~/bar       # error
    """
    if dest is None:
        dest = Path.cwd()
        download(ctx, source, dest)
    else:
        prefix = ctx.obj.config.get("file", "path_prefix") + ":"
        input_is_local = not source.startswith(prefix)
        output_is_local = not dest.startswith(prefix)
        if input_is_local and output_is_local:
            ctx.fail("input and output path is local!")
        if not input_is_local and not output_is_local:
            ctx.fail("input and output path is remote!")

        if input_is_local:
            source = Path(source)
            if not source.exists():
                print("src path does not exist")
                ctx.exit(1)
            upload(ctx, source, dest)
        else:
            dest = Path(dest).expanduser().resolve()
            download(ctx, source, dest, force)


@file_app.command(short_help="Upload file")
def upload(
    ctx: Context,
    source: Path = Argument(..., exists=True),
    dest: str = Argument(...),
) -> None:
    """Upload local source to remote dest

    WARNING: existing file will be replaced!
    """
    source = source.expanduser().resolve()
    dest = resolve(ctx, dest)
    output = get_remote_output_path(str(source), dest)
    try:
        data = source.read_bytes()
    except IOError:  # pragma: no cover
        print(f"Can't read {source}")
        ctx.abort()
    result = ctx.obj.api.file.upload(output, data)
    process_result(result, expected_status=[200, 201], print_content=False)


@file_app.command(short_help="Download file")
def download(
    ctx: Context,
    source: str = Argument(...),
    dest: Path = Argument(Path.cwd(), show_default=False),
    force: bool = Option(
        False,
        "--force",
        "-f",
        is_flag=True,
        help="Ignore existing file",
    ),
) -> None:
    """Download remote source to local dest"""

    source = resolve(ctx, source)
    dest = get_local_output_path(source, str(dest), force)
    if dest is None:
        print("dest path exist")
        ctx.exit(1)
    result = ctx.obj.api.file.get_content(source)
    process_result(result, print_content=False)
    if not isinstance(result.content, bytes):
        print(f"{source} not a file")
        ctx.exit(1)
    try:
        dest.write_bytes(result.content)
    except IOError:  # pragma: no cover
        print(f"Can't write in {dest}")
        ctx.exit(1)


@file_app.command(short_help="Remove content")
def rm(ctx: Context, path: str = PATH_REMOTE_ARGUMENT) -> None:
    """Remove files and directories

    NOTE: directory will be removed recursively.
    """

    result = ctx.obj.api.file.delete(path)
    process_result(result, expected_status=204, print_content=False)


@file_app.command()
def ls(
    ctx: Context,
    path: str = PATH_REMOTE_ARGUMENT,
    json: bool = Option(False, "--json", is_flag=True, help="JSON output"),
) -> None:
    """List directory contents"""

    result = ctx.obj.api.file.get_content(path)
    formatter = DirectoryFormatter() if not json else None
    process_result(result, formatter=formatter)


@file_app.command()
def cat(ctx: Context, path: str = PATH_REMOTE_ARGUMENT) -> None:
    """Show file content"""

    result = ctx.obj.api.file.get_content(path)
    process_result(result, formatter=ContentFormatter())


@file_app.command(short_help="Path sharing status")
def share(
    ctx: Context,
    path: str = PATH_REMOTE_ARGUMENT,
    update: Optional[bool] = Option(
        None,
        "--start/--stop",
        is_flag=True,
        help="Start/Stop sharing",
    ),
) -> None:
    """Get or update current sharing status for a path"""

    api = ctx.obj.api.file
    if update is not None:
        if update:
            result = api.start_sharing(path)
            status = [200, 201]
        else:
            result = api.stop_sharing(path)
            status = 204
    else:
        result = api.get_sharing_status(path)
        status = 200
    process_result(result, expected_status=status)


@file_app.command()
def tree(ctx: Context, path: str = PATH_REMOTE_ARGUMENT) -> None:
    """List directory contents (recursively)"""

    result = ctx.obj.api.file.get_tree(path)
    process_result(result)
