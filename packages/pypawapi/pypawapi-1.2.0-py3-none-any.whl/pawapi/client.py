__all__ = ["Client"]

from typing import Dict
from typing import Optional
from typing import Union

import requests

from .abc import AbstractClient
from .exceptions import InvalidJSONError
from .exceptions import InvalidTokenError
from .exceptions import NotFoundError
from .exceptions import PermissionDeniedError
from .exceptions import RequestTimeoutError
from .exceptions import StatusError
from .region import Region
from .response import Content
from .response import Response
from .utils import validate_credentials


class Client(AbstractClient):

    __slots__ = (
        "_url",
        "_headers",
        "_raise_404",
        "_timeout",
    )

    def __init__(
        self,
        username: str,
        token: str,
        region: Region,
        raise_404: bool,
        timeout: float,
    ) -> None:
        validate_credentials("username", username)
        validate_credentials("token", token)
        prefix = "eu" if region == Region.EU else "www"
        self._url = f"https://{prefix}.pythonanywhere.com/api/v0/user/{username}"  # noqa: E501
        self._headers = {"Authorization": f"Token {token}"}
        self._raise_404 = raise_404
        self._timeout = timeout

    def _request(
        self,
        method: str,
        path: str,
        *,
        data: Optional[Dict[str, Optional[Union[str, int]]]] = None,
        params: Optional[Dict[str, Optional[Union[str, int]]]] = None,
        files: Optional[Dict[str, bytes]] = None,
    ) -> Response:
        try:
            response = requests.request(
                method=method,
                url=f"{self._url}/{path}",
                params=params,
                data=data,
                files=files,
                headers=self._headers,
                timeout=self._timeout,
            )
        except requests.Timeout:
            raise RequestTimeoutError(
                f"Request timed out (timeout={self._timeout})"
            ) from None

        return self._check_response(response)

    def _check_status(self, response: requests.Response) -> None:
        status = response.status_code
        if status >= 400:
            try:
                json = response.json()
                error = json.get("error", None)
                detail = json.get("detail", None)
                description = error if error is not None else detail
            except requests.JSONDecodeError:
                description = None

            if status == 401:
                raise InvalidTokenError(
                    status_code=401,
                    description=description,
                    raw_content=response.content,
                )
            elif status == 403:
                raise PermissionDeniedError(
                    status_code=403,
                    description=description,
                    raw_content=response.content,
                )
            elif status == 404:
                if self._raise_404:
                    raise NotFoundError(
                        status_code=404,
                        description=description,
                        raw_content=response.content,
                    )
            else:
                raise StatusError(
                    status_code=status,
                    description=description,
                    raw_content=response.content
                )

    def _check_response(self, response: requests.Response) -> Response:
        self._check_status(response)
        content: Optional[Content] = None
        content_type = response.headers.get("Content-Type", None)
        if content_type is not None:
            if response.content:
                # response from /webapps with "text/json" in Content-Type
                if ("application/json" in content_type
                        or "text/json" in content_type):  # noqa: W503
                    try:
                        content = response.json()
                    except requests.JSONDecodeError:
                        raise InvalidJSONError(
                            f"Got invalid json: {response.content!r}"
                        ) from None
                elif "application/octet-stream" in content_type:
                    content = response.content
        return Response(status=response.status_code, content=content)

    def get(
        self,
        path: str,
        params: Optional[Dict[str, Optional[Union[str, int]]]] = None,
    ) -> Response:
        return self._request("get", path, params=params)

    def post(
        self,
        path: str,
        *,
        data: Optional[Dict[str, Optional[Union[str, int]]]] = None,
        files: Optional[Dict[str, bytes]] = None,
    ) -> Response:
        return self._request("post", path, data=data, files=files)

    def patch(
        self,
        path: str,
        data: Optional[Dict[str, Optional[Union[str, int]]]] = None,
    ) -> Response:
        return self._request("patch", path, data=data)

    def delete(
        self,
        path: str,
        params: Optional[Dict[str, Optional[Union[str, int]]]] = None,
    ) -> Response:
        return self._request("delete", path, params=params)
