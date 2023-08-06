import pytest
from responses import RequestsMock

from pawapi import Pawapi


@pytest.fixture(scope="session")
def test_user() -> str:
    return "testUser"


@pytest.fixture(scope="session")
def test_token() -> str:
    return "testToken"


@pytest.fixture
def pawapi(test_user: str, test_token: str) -> Pawapi:
    return Pawapi(test_user, test_token)


@pytest.fixture
def paw_api_client(pawapi: Pawapi, request: pytest.FixtureRequest) -> None:
    request.cls.api = pawapi
    request.cls.url = pawapi._client._url


@pytest.fixture
def mock_responses() -> RequestsMock:
    with RequestsMock() as r:
        yield r
