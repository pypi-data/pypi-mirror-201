from __future__ import annotations

from pathlib import Path
from typing import Optional
from typing import Union

from typer import Context


def resolve(ctx: Context, path: str) -> str:
    path_prefix: str = ctx.obj.config.get("file", "path_prefix") + ":"
    # pa:~/foo -> ~/foo
    if path.startswith(path_prefix):
        path = path[len(path_prefix):]

    username = ctx.obj.credentials.username

    # ~/foo | ~foo -> /home/user/foo
    if path.startswith("~"):
        path = path[1:]
        if path.startswith("/"):
            path = path[1:]
        path = f"/home/{username}/{path}"
        return path

    # foo -> /foo
    if not path.startswith("/"):
        path = f"/{path}"

    url_prefix = f"/user/{username}/files"

    # /home/localusername/foo -> /home/username/foo
    if path.startswith("/home"):
        path_split = path[1:].split("/")
        if len(path_split) > 1:
            path_split[1] = username
            path = "/" + "/".join(path_split)

    # /user/username/files/foo/bar -> /foo/bar
    elif path.startswith(url_prefix):
        path = path.replace(url_prefix, "")

    return path


def get_file_name(path: str) -> str:
    return path.rsplit("/", maxsplit=1)[-1]


def get_local_output_path(
    src_path: str,
    dest_path: Union[Path, str],
    force: bool,
) -> Optional[Path]:
    if isinstance(dest_path, str):
        dest_path = Path(dest_path)
    if dest_path.exists():
        if not dest_path.is_dir():
            if not force:
                return None
            return dest_path
        file_name = get_file_name(src_path)
        dest_path = dest_path / file_name
    return dest_path


def get_remote_output_path(
    src_path: str,
    dest_path: str,
) -> str:
    if dest_path.endswith("/"):
        file_name = get_file_name(src_path)
        dest_path = f"{dest_path}{file_name}"
    return dest_path
