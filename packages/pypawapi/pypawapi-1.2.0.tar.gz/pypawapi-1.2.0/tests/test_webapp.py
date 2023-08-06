from typing import TYPE_CHECKING
from typing import Dict
from typing import Union

import pytest
from responses.matchers import urlencoded_params_matcher

from pawapi.python import Python3

if TYPE_CHECKING:
    from responses import RequestsMock


@pytest.fixture
def params_static_files() -> Dict[str, str]:
    return {
        "url": "/static",
        "path": "/home/user/static",
    }


@pytest.fixture
def params_static_headers() -> Dict[str, str]:
    return {
        "url": "/header",
        "name": "headername",
        "value": "headervalue",
    }


@pytest.fixture(params=(55, "55"))
def file_id(request: pytest.FixtureRequest) -> Union[int, str]:
    return request.param


@pytest.fixture(params=(44, "44"))
def header_id(request: pytest.FixtureRequest) -> Union[int, str]:
    return request.param


@pytest.mark.usefixtures("paw_api_client")
class TestWebApp:
    domain = "test.domain.site"
    file_id = 321
    header_id = 123

    def test_list(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.get(f"{self.url}/webapps/")
        self.api.webapp.list()

    def test_create(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.post(
            url=f"{self.url}/webapps/",
            match=(
                urlencoded_params_matcher({
                    "domain_name": self.domain,
                    "python_version": "python38",
                }),
            ),
        )
        self.api.webapp.create(
            domain_name=self.domain,
            python_version=Python3.PYTHON38,
        )

    def test_info(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.get(f"{self.url}/webapps/{self.domain}/")
        self.api.webapp.get_info(self.domain)

    def test_update(self, mock_responses: 'RequestsMock') -> None:
        params = {
            "source_directory": "/home/user/appsrc",
            "virtualenv_path": "/home/user/venv",
            "force_https": True,
        }
        mock_responses.patch(
            url=f"{self.url}/webapps/{self.domain}/",
            match=(
                urlencoded_params_matcher({
                    "python_version": "3.9",
                    **{k: str(v)
                       for k, v in params.items()}
                }),
            ),
        )
        self.api.webapp.update(
            domain_name=self.domain,
            python_version=Python3.PYTHON39,
            **params,
        )

    def test_update_protected(self, mock_responses: 'RequestsMock') -> None:
        user = "username"
        pwd = "password123"

        mock_responses.patch(
            url=f"{self.url}/webapps/{self.domain}/",
            match=(
                urlencoded_params_matcher({
                    "password_protection_enabled": "True",
                    "password_protection_username": user,
                    "password_protection_password": pwd,
                }),
            ),
        )
        self.api.webapp.update(
            domain_name=self.domain,
            protection=True,
            protection_username=user,
            protection_password=pwd,
        )

    def test_delete(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.delete(f"{self.url}/webapps/{self.domain}/")
        self.api.webapp.delete(self.domain)

    def test_enable(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.post(f"{self.url}/webapps/{self.domain}/enable/")
        self.api.webapp.enable(self.domain)

    def test_disable(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.post(f"{self.url}/webapps/{self.domain}/disable/")
        self.api.webapp.disable(self.domain)

    def test_reload(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.post(f"{self.url}/webapps/{self.domain}/reload/")
        self.api.webapp.reload(self.domain)

    def test_ssl_info(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.get(f"{self.url}/webapps/{self.domain}/ssl/")
        self.api.webapp.get_ssl_info(self.domain)

    def test_add_ssl(self, mock_responses: 'RequestsMock') -> None:
        params = {
            "cert": "cert",
            "private_key": "privete_key",
        }
        mock_responses.post(
            url=f"{self.url}/webapps/{self.domain}/ssl/",
            match=(urlencoded_params_matcher(params), ),
        )
        self.api.webapp.add_ssl(domain_name=self.domain, **params)

    def test_delete_ssl(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.delete(f"{self.url}/webapps/{self.domain}/ssl/")
        self.api.webapp.delete_ssl(self.domain)

    def test_list_static_files(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.get(f"{self.url}/webapps/{self.domain}/static_files/")
        self.api.webapp.list_static_files(self.domain)

    def test_add_static_file(
        self,
        mock_responses: 'RequestsMock',
        params_static_files: Dict[str, str],
    ) -> None:
        mock_responses.post(
            url=f"{self.url}/webapps/{self.domain}/static_files/",
            match=(urlencoded_params_matcher(params_static_files), ),
        )
        self.api.webapp.add_static_file(
            domain_name=self.domain,
            **params_static_files,
        )

    def test_static_file_info(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.get(
            f"{self.url}/webapps/{self.domain}/static_files/{self.file_id}/",
        )
        self.api.webapp.get_static_file_info(self.domain, self.file_id)

    def test_update_static_file(
        self,
        mock_responses: 'RequestsMock',
        params_static_files: Dict[str, str],
    ) -> None:
        mock_responses.patch(
            url=f"{self.url}/webapps/{self.domain}/static_files/{self.file_id}/",  # noqa: E501
            match=(urlencoded_params_matcher(params_static_files), ),
        )  # yapf: disable
        self.api.webapp.update_static_file(
            domain_name=self.domain,
            file_id=self.file_id,
            **params_static_files,
        )

    def test_delete_static_file(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.delete(
            f"{self.url}/webapps/{self.domain}/static_files/{self.file_id}/",
        )
        self.api.webapp.delete_static_file(self.domain, self.file_id)

    def test_list_static_headers(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.get(f"{self.url}/webapps/{self.domain}/static_headers/")
        self.api.webapp.list_static_headers(self.domain)

    def test_add_static_header(
        self,
        mock_responses: 'RequestsMock',
        params_static_headers: Dict[str, str]
    ) -> None:
        mock_responses.post(
            url=f"{self.url}/webapps/{self.domain}/static_headers/",
            match=(urlencoded_params_matcher(params_static_headers), ),
        )
        self.api.webapp.add_static_header(
            domain_name=self.domain,
            **params_static_headers,
        )

    def test_static_header_info(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.get(
            f"{self.url}/webapps/{self.domain}/static_headers/{self.header_id}/",  # noqa: E501
        )
        self.api.webapp.get_static_header_info(self.domain, self.header_id)

    def test_update_static_header(
        self,
        mock_responses: 'RequestsMock',
        params_static_headers: Dict[str, str],
    ) -> None:
        mock_responses.patch(
            url=f"{self.url}/webapps/{self.domain}/static_headers/{self.header_id}/",  # noqa: E501
            match=(urlencoded_params_matcher(params_static_headers), ),
        )  # yapf: disable
        self.api.webapp.update_static_header(
            domain_name=self.domain,
            header_id=self.header_id,
            **params_static_headers,
        )

    def test_delete_static_header(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.delete(
            f"{self.url}/webapps/{self.domain}/static_headers/{self.header_id}/",  # noqa: E501
        )
        self.api.webapp.delete_static_header(self.domain, self.header_id)
