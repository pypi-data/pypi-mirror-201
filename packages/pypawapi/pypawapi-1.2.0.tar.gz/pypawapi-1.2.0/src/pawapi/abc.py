__all__ = ["AbstractClient"]

from abc import ABC
from abc import abstractmethod
from typing import Dict
from typing import Optional
from typing import Union

from .response import Response


class AbstractClient(ABC):

    __slots__ = ()

    @abstractmethod
    def get(
        self,
        path: str,
        params: Optional[Dict[str, Optional[Union[str, int]]]] = None,
    ) -> Response:
        pass

    @abstractmethod
    def post(
        self,
        path: str,
        *,
        data: Optional[Dict[str, Optional[Union[str, int]]]] = None,
        files: Optional[Dict[str, bytes]] = None,
    ) -> Response:
        pass

    @abstractmethod
    def patch(
        self,
        path: str,
        data: Optional[Dict[str, Optional[Union[str, int]]]] = None,
    ) -> Response:
        pass

    @abstractmethod
    def delete(
        self,
        path: str,
        params: Optional[Dict[str, Optional[Union[str, int]]]] = None,
    ) -> Response:
        pass
