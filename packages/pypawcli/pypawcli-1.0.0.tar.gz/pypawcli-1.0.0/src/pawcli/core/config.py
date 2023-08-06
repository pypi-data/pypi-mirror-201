from __future__ import annotations

from configparser import ConfigParser
from pathlib import Path
from typing import Optional

from typer import get_app_dir

APP_NAME = "pawcli"
APP_DIR = Path(get_app_dir(APP_NAME))


class Config(ConfigParser):

    def __init__(self, *, config: Optional[Path] = None) -> None:
        super().__init__(
            allow_no_value=True,
            defaults={
                "timeout": 16,
                "region": "us",
                "python": 39,
                "default_shell": "bash",
                "path_prefix": "pa",
            },
        )

        self.add_section("api")
        self.add_section("webapp")
        self.add_section("console")
        self.add_section("file")
        self.add_section("task")

        self.file = config if config is not None else APP_DIR / "config.ini"
        if self.file.exists():
            self.read(str(self.file))

    def write(self, fp, space_around_delimiters: bool = True):
        """write config without defaults and empty sections"""

        d = self._delimiters[0]
        if space_around_delimiters:
            d = f" {d} "

        for section, options in self._sections.items():
            if options:
                self._write_section(fp, section, options.items(), d)
