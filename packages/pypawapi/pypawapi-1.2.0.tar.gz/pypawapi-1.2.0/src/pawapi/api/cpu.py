__all__ = ["Cpu"]

from pawapi.response import Response

from .base import BaseEndpoint


class Cpu(BaseEndpoint):
    __endpoint = "cpu"

    __slots__ = ()

    def get_info(self) -> Response:
        """ Information about cpu usage """

        return self._client.get(f"{self.__endpoint}/")
