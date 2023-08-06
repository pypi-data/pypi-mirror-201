__all__ = ["BaseEndpoint"]

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from pawapi.abc import AbstractClient


class BaseEndpoint:
    __slots__ = "_client"

    def __init__(self, client: "AbstractClient") -> None:
        self._client = client

    def __repr__(self) -> str:  # pragma: no cover
        return f"<{self.__class__.__name__}>"
