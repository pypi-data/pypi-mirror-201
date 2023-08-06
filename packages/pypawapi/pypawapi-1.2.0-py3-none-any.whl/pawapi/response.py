__all__ = ["Response"]

from dataclasses import dataclass
from typing import Dict
from typing import Optional
from typing import Union

Content = Union[Dict[str, Union[str, int, bytes]], bytes]


@dataclass(frozen=True)
class Response:
    status: int
    content: Optional[Content] = None
