__all__ = ["Students"]

from pawapi.response import Response

from .base import BaseEndpoint


class Students(BaseEndpoint):
    __endpoint = "students"

    __slots__ = ()

    def list(self) -> Response:
        """ List of students """

        return self._client.get(f"{self.__endpoint}/")

    def delete(self, student: str) -> Response:
        """ Delete a student """

        return self._client.delete(f"{self.__endpoint}/{student}/")
