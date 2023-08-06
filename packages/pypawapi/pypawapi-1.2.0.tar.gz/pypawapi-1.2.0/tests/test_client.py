import json
from typing import TYPE_CHECKING
from typing import Union

import pytest
from requests.exceptions import Timeout
from responses.matchers import header_matcher

from pawapi.abc import AbstractClient
from pawapi.client import Client
from pawapi.exceptions import InvalidCredentialsError
from pawapi.exceptions import InvalidTokenError
from pawapi.exceptions import NotFoundError
from pawapi.exceptions import PermissionDeniedError
from pawapi.exceptions import RequestTimeoutError
from pawapi.exceptions import StatusError
from pawapi.region import Region
from pawapi.utils import validate_credentials

if TYPE_CHECKING:
    from respsonses import RequestsMock


@pytest.fixture(scope="class")
def client(test_user: str, test_token: str) -> AbstractClient:
    return Client(test_user, test_token, Region.US, False, 8)


def test_region() -> None:
    assert Region.US.value == "us"
    assert Region.EU.value == "eu"


@pytest.mark.parametrize(
    "value",
    (
        "user_name",
        "username!",
        "",
        123,
        " ",
        "u   ",
        b"username",
        " username",
        None,
        "@username",
        "usern#21ame",
    ),
)
def test_validate_invalid_credentials(value):
    with pytest.raises(InvalidCredentialsError):
        validate_credentials("invalid", value)


@pytest.mark.parametrize(
    "value",
    (
        "username",
        "username1",
        "user1name",
        "1234567890",
    ),
)
def test_validate_valid_credentials(value):
    validate_credentials("valid", value)


class TestBaseClient:

    @pytest.mark.parametrize(
        "region,url",
        (
            (
                Region.US,
                "https://www.pythonanywhere.com/api/v0/user/",
            ),
            (
                Region.EU,
                "https://eu.pythonanywhere.com/api/v0/user/",
            ),
        )
    )
    def test_api_url(
        self,
        test_user: str,
        test_token: str,
        region: Region,
        url: str,
    ) -> None:
        client = Client(
            test_user,
            test_token,
            region=region,
            raise_404=False,
            timeout=8,
        )
        assert client._url == url + test_user

    def test_api_auth_header(
        self, client: AbstractClient, test_token: str
    ) -> None:
        assert client._headers.get(
            "Authorization", None
        ) == f"Token {test_token}"

    @pytest.mark.parametrize("content_type", ("application/json", "text/json"))
    def test_response_json(
        self,
        mock_responses: 'RequestsMock',
        client: AbstractClient,
        test_token: str,
        content_type: str,
    ) -> None:
        json_params = {
            "list": [1, 2, 3, 4],
            "dict": {
                "key1": "value1",
                "key2": "value2",
            },
            "int": 12,
            "str": "str",
        }

        mock_responses.get(
            url=f"{client._url}/json/",
            content_type=content_type,
            body=json.dumps(json_params),
            match=(header_matcher({"Authorization": f"Token {test_token}"}), ),
        )
        resp = client.get("json/")
        assert resp.content == json_params

    @pytest.mark.parametrize(
        "content_type,body,result",
        (
            ("application/octet-stream", b"content", b"content"),
            ("application/json", b"", None),
            ("text/html", b"<h>html here</h>", None),
        )
    )
    def test_response_content(
        self,
        mock_responses: 'RequestsMock',
        client: AbstractClient,
        content_type: str,
        test_token: str,
        body: bytes,
        result: Union[bytes, None],
    ) -> None:
        mock_responses.get(
            url=f"{client._url}/content/",
            body=body,
            content_type=content_type,
            match=(header_matcher({"Authorization": f"Token {test_token}"}), ),
        )
        resp = client.get("content/")
        assert resp.content == result

    def test_response_error_401(
        self,
        mock_responses: 'RequestsMock',
        client: AbstractClient,
        test_token: str,
    ) -> None:
        url = "access401/"
        error = "Invalid token."
        mock_responses.get(
            url=f"{client._url}/{url}",
            json={"detail": error},
            status=401,
            match=(header_matcher({"Authorization": f"Token {test_token}"}), ),
        )
        with pytest.raises(InvalidTokenError, match=f"401, {error}"):
            client.get(url)

    def test_response_error_403(
        self,
        mock_responses: 'RequestsMock',
        client: AbstractClient,
    ) -> None:
        url = "access403/"
        error = "permission error details"
        mock_responses.get(
            url=f"{client._url}/{url}",
            json={"detail": error},
            status=403,
        )
        with pytest.raises(PermissionDeniedError, match=f"403, {error}"):
            client.get(url)

    @pytest.mark.parametrize("status", (201, 204, 404))
    def test_response(
        self,
        mock_responses: 'RequestsMock',
        client: AbstractClient,
        status: int,
    ) -> None:
        mock_responses.get(url=f"{client._url}/access/", status=status)
        response = client.get("access/")
        assert response.status == status

    def test_response_raise_404(
        self,
        mock_responses: 'RequestsMock',
        client: AbstractClient,
    ) -> None:
        client._raise_404 = True
        mock_responses.get(url=f"{client._url}/access/", status=404)
        with pytest.raises(NotFoundError):
            client.get("access/")

    def test_response_raise_timeout_eror(
        self,
        mock_responses: 'RequestsMock',
        client: AbstractClient,
    ) -> None:
        mock_responses.get(url=f"{client._url}/timeout/", body=Timeout())
        with pytest.raises(RequestTimeoutError):
            client.get("timeout/")

    def test_response_raise_status_empty(
        self,
        mock_responses: 'RequestsMock',
        client: AbstractClient,
    ) -> None:
        mock_responses.get(url=f"{client._url}/status/", status=400)
        with pytest.raises(StatusError, match="400"):
            client.get("status/")

    def test_response_raise_status_description(
        self,
        mock_responses: 'RequestsMock',
        client: AbstractClient,
    ) -> None:
        mock_responses.get(
            url=f"{client._url}/status/",
            status=418,
            json={"error": "I'm a teapot"},
        )
        with pytest.raises(StatusError, match="418, I'm a teapot"):
            client.get("status/")
