from __future__ import annotations

import json as jsonlib
from abc import ABC
from abc import abstractmethod


class AbstractFormatter(ABC):
    __slots__ = ()

    @abstractmethod
    def __call__(self, content) -> str:
        pass


class JsonFormatter(AbstractFormatter):  # pragma: no cover
    __slots__ = "indent"

    def __init__(self, indent: int = 2) -> None:
        self.indent = indent

    def __call__(self, content) -> str:
        if isinstance(content, (dict, list)):
            return jsonlib.dumps(content, indent=self.indent)


class DirectoryFormatter(AbstractFormatter):  # pragma: no cover
    __slots__ = ()

    def __call__(self, content) -> str:
        if not isinstance(content, dict):
            return "not a directory"

        dirs = []
        files = []
        for k, v in content.items():
            if v["type"] == "file":
                files.append(k)
            else:
                dirs.append(f"{k}/")

        result = ""
        if dirs:
            result += "\n".join(d for d in sorted(dirs))
            result += "\n"
        if files:
            result += "\n".join(f for f in sorted(files))
        if result.endswith("\n"):
            result = result[:-1]
        return result


class ContentFormatter(AbstractFormatter):  # pragma: no cover
    __slots__ = ()

    def __call__(self, content) -> str:
        if not isinstance(content, bytes):
            return "not a file"
        return content.decode()
