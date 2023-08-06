__all__ = ["Python"]

from typing import Union

from pawapi.python import Python2
from pawapi.python import Python3
from pawapi.response import Response

from .base import BaseEndpoint


class Python(BaseEndpoint):
    __slots__ = ()

    def get_python_version(self) -> Response:
        """ Information about current and available default Python version """

        return self._client.get("default_python_version/")

    def set_python_version(self, version: Union[Python2, Python3]) -> Response:
        """ Set default Python version """

        return self._client.patch(
            path="default_python_version/",
            data={
                "default_python_version": version.format_value(short=True),
            },
        )

    def get_python3_version(self) -> Response:
        """ Information about current and available default Python 3 version """

        return self._client.get("default_python3_version/")

    def set_python3_version(self, version: Python3) -> Response:
        """ Set default Python 3 version """

        return self._client.patch(
            path="default_python3_version/",
            data={
                "default_python3_version": version.format_value(short=True),
            },
        )

    def get_sar_version(self) -> Response:
        """ Information about current and available Python
            version used for the 'Run' button in the editor
        """

        return self._client.get("default_save_and_run_python_version/")

    def set_sar_version(self, version: Python3) -> Response:
        """ Set Python version used for the 'Run' button in the editor """

        return self._client.patch(
            path="default_save_and_run_python_version/",
            data={
                "default_save_and_run_python_version": version.format_value(
                    short=True
                ),
            },
        )
