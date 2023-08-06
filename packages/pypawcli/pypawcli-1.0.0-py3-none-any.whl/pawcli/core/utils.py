from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from typer import Context


def save_config(ctx: Context) -> None:
    cfg = ctx.obj.config
    try:
        if not cfg.file.parent.exists():
            cfg.file.parent.mkdir()
        with cfg.file.open("w") as f:
            cfg.write(f)
    except IOError as error:
        print(f"Can't save config: {error}")
        ctx.exit(1)
