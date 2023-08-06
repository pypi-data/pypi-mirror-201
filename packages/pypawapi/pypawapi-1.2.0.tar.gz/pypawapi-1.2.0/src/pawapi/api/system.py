__all__ = ["System"]

from pawapi.response import Response
from pawapi.system import SystemImage

from .base import BaseEndpoint


class System(BaseEndpoint):
    __endpoint = "system_image"

    __slots__ = ()

    def get_current_image(self) -> Response:
        """ Information about current and available system images """

        return self._client.get(f"{self.__endpoint}/")

    def set_image(self, system_image: SystemImage) -> Response:
        """ Set system image """

        return self._client.patch(
            path=f"{self.__endpoint}/",
            data={"system_image": system_image.value},
        )
