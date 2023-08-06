from pawapi import Python2
from pawapi import Python3

from pawcli.core.enum import AppLog
from pawcli.core.enum import Python3Version
from pawcli.core.enum import PythonVersion


def test_python_version():
    assert PythonVersion.PY310.value == "310"
    assert PythonVersion.PY39.value == "39"
    assert PythonVersion.PY38.value == "38"
    assert PythonVersion.PY37.value == "37"
    assert PythonVersion.PY36.value == "36"
    assert PythonVersion.PY27.value == "27"


def test_python3_version():
    assert Python3Version.PY310.value == "310"
    assert Python3Version.PY39.value == "39"
    assert Python3Version.PY38.value == "38"
    assert Python3Version.PY37.value == "37"
    assert Python3Version.PY36.value == "36"


def test_long_version():
    assert PythonVersion.PY310.to_long_version() == "python3.10"
    assert PythonVersion.PY27.to_long_version() == "python2.7"
    assert Python3Version.PY37.to_long_version() == "python3.7"


def test_as_external():
    assert PythonVersion.PY310.as_external() is Python3.PYTHON310
    assert PythonVersion.PY27.as_external() is Python2.PYTHON27
    assert Python3Version.PY37.as_external() is Python3.PYTHON37


def test_app_log():
    assert AppLog.ACCESS.value == "access"
    assert AppLog.ERROR.value == "error"
    assert AppLog.SERVER.value == "server"
