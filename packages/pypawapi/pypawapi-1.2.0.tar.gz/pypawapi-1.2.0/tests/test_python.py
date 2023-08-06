from typing import TYPE_CHECKING

import pytest
from responses.matchers import urlencoded_params_matcher

from pawapi.python import Python2
from pawapi.python import Python3

if TYPE_CHECKING:
    from responses import RequestsMock


@pytest.mark.usefixtures("paw_api_client")
class TestPython:

    def test_get_python_version(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.get(f"{self.url}/default_python_version/")
        self.api.python.get_python_version()

    def test_set_python_version(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.patch(
            url=f"{self.url}/default_python_version/",
            match=(
                urlencoded_params_matcher({"default_python_version": "2.7"}),
            ),
        )
        self.api.python.set_python_version(Python2.PYTHON27)

    def test_get_python3_version(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.get(f"{self.url}/default_python3_version/")
        self.api.python.get_python3_version()

    def test_set_python3_version(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.patch(
            url=f"{self.url}/default_python3_version/",
            match=(
                urlencoded_params_matcher({"default_python3_version": "3.8"}),
            ),
        )
        self.api.python.set_python3_version(Python3.PYTHON38)

    def test_get_python_sar_version(
        self, mock_responses: 'RequestsMock'
    ) -> None:
        mock_responses.get(f"{self.url}/default_save_and_run_python_version/")
        self.api.python.get_sar_version()

    def test_set_python_sar_version(
        self, mock_responses: 'RequestsMock'
    ) -> None:
        mock_responses.patch(
            url=f"{self.url}/default_save_and_run_python_version/",
            match=(
                urlencoded_params_matcher({
                    "default_save_and_run_python_version": "3.7",
                }),
            ),
        )
        self.api.python.set_sar_version(Python3.PYTHON37)
