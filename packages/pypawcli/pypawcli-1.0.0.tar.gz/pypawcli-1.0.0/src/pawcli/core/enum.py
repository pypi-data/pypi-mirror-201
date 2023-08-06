from __future__ import annotations

from enum import Enum
from typing import Union

from pawapi import Python2
from pawapi import Python3


class _PythonVersionEnum(Enum):

    def to_long_version(self) -> str:
        value = self.value
        return f"python{value[0]}.{value[1:]}"

    def as_external(self) -> Union[Python2, Python3]:
        if self.value == "27":
            return Python2.PYTHON27
        return Python3(self.to_long_version())


class PythonVersion(_PythonVersionEnum):
    PY310 = "310"
    PY39 = "39"
    PY38 = "38"
    PY37 = "37"
    PY36 = "36"
    PY27 = "27"


class Python3Version(_PythonVersionEnum):
    PY310 = "310"
    PY39 = "39"
    PY38 = "38"
    PY37 = "37"
    PY36 = "36"


class AppLog(Enum):
    ACCESS = "access"
    ERROR = "error"
    SERVER = "server"
