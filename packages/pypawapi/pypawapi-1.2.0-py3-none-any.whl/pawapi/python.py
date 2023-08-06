__all__ = [
    "Python2",
    "Python3",
]

from enum import Enum


class _PythonEnum(Enum):

    def format_value(self, *, short: bool = False, dot: bool = True) -> str:
        ret: str = self.value
        if short:
            ret = ret[6:]
        if not dot:
            ret = ret.replace(".", "")
        return ret


class Python2(_PythonEnum):
    PYTHON27 = "python2.7"


class Python3(_PythonEnum):
    PYTHON310 = "python3.10"
    PYTHON39 = "python3.9"
    PYTHON38 = "python3.8"
    PYTHON37 = "python3.7"
    PYTHON36 = "python3.6"
