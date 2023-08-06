__all__ = ["Console"]

from typing import Optional
from typing import Union

from pawapi.python import Python3
from pawapi.response import Response
from pawapi.shell import Shell

from .base import BaseEndpoint


class Console(BaseEndpoint):
    __endpoint = "consoles"

    __slots__ = ()

    def list(self) -> Response:
        """ List all consoles """

        return self._client.get(f"{self.__endpoint}/")

    def list_shared(self) -> Response:
        """ List all consoles shared with you """

        return self._client.get(f"{self.__endpoint}/shared_with_you/")

    def create(
        self,
        executable: Union[Shell, Python3],
        *,
        arguments: Optional[str] = None,
        working_directory: Optional[str] = None,
    ) -> Response:
        """ Create a new console

            NOTE: does not actually start the process!
        """

        return self._client.post(
            path=f"{self.__endpoint}/",
            data={
                "executable": executable.value,
                "arguments": arguments,
                "working_directory": working_directory,
            },
        )

    def get_info(self, console_id: Union[int, str]) -> Response:
        """ Information about a console """

        return self._client.get(f"{self.__endpoint}/{console_id}/")

    def kill(self, console_id: Union[int, str]) -> Response:
        """ Kill a console """

        return self._client.delete(f"{self.__endpoint}/{console_id}/")

    def get_output(self, console_id: Union[int, str]) -> Response:
        """ Get recent output from the console (max 500 characters) """

        return self._client.get(
            f"{self.__endpoint}/{console_id}/get_latest_output/"
        )

    def send_input(
        self,
        console_id: Union[int, str],
        input_: str,
    ) -> Response:
        """ 'type' command into the console.

            NOTE: Add a '\\n' for 'press enter'
        """

        return self._client.post(
            path=f"{self.__endpoint}/{console_id}/send_input/",
            data={"input": input_},
        )
