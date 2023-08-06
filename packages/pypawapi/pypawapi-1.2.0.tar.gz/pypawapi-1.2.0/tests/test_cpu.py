from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from responses import RequestsMock


@pytest.mark.usefixtures("paw_api_client")
class TestCpu:

    def test_info(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.get(f"{self.url}/cpu/")
        self.api.cpu.get_info()
