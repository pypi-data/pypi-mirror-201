from typing import Union

import pytest

from pawapi.python import Python2
from pawapi.python import Python3
from pawapi.shell import Shell


def test_console_executable() -> None:
    assert Shell.BASH.value == "bash"
    assert Shell.MYSQL.value == "mysql"
    assert Shell.IPYTHON310.value == "ipython3.10"
    assert Shell.IPYTHON39.value == "ipython3.9"
    assert Shell.IPYTHON38.value == "ipython3.8"
    assert Shell.IPYTHON37.value == "ipython3.7"
    assert Shell.IPYTHON36.value == "ipython3.6"
    assert Shell.PYPY2.value == "pypy2"
    assert Shell.PYPY3.value == "pypy3"


def test_python2_version() -> None:
    assert Python2.PYTHON27.value == "python2.7"


def test_python3_version() -> None:
    assert Python3.PYTHON310.value == "python3.10"
    assert Python3.PYTHON39.value == "python3.9"
    assert Python3.PYTHON38.value == "python3.8"
    assert Python3.PYTHON37.value == "python3.7"
    assert Python3.PYTHON36.value == "python3.6"


@pytest.mark.parametrize(
    "version,result",
    (
        (Python3.PYTHON310, "3.10"),
        (Python3.PYTHON39, "3.9"),
        (Python3.PYTHON37, "3.7"),
        (Python2.PYTHON27, "2.7"),
    )
)
def test_format_version_short(
    version: Union[Python2, Python3], result: str
) -> None:
    assert version.format_value(short=True) == result


@pytest.mark.parametrize(
    "version,result",
    (
        (Python3.PYTHON310, "python310"),
        (Python3.PYTHON39, "python39"),
        (Python3.PYTHON37, "python37"),
        (Python2.PYTHON27, "python27"),
    )
)
def test_format_version_no_dot(
    version: Union[Python2, Python3], result: str
) -> None:
    assert version.format_value(dot=False) == result


@pytest.mark.parametrize(
    "version,result",
    (
        (Python3.PYTHON310, "310"),
        (Python3.PYTHON39, "39"),
        (Python3.PYTHON37, "37"),
        (Python2.PYTHON27, "27"),
    )
)
def test_format_version_short_no_dot(
    version: Union[Python2, Python3], result: str
) -> None:
    assert version.format_value(short=True, dot=False) == result
