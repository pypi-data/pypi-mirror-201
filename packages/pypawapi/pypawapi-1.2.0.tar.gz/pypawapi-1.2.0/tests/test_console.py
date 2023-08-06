from typing import TYPE_CHECKING
from typing import Dict
from typing import Union

import pytest
from responses.matchers import urlencoded_params_matcher

from pawapi.python import Python3
from pawapi.shell import Shell

if TYPE_CHECKING:
    from responses import RequestsMock


@pytest.fixture
def params_create() -> Dict[str, str]:
    return {
        "executable": "python3.9",
        "working_directory": "/home",
    }


@pytest.fixture(params=(10, "10"))
def console_id(request: pytest.FixtureRequest) -> Union[int, str]:
    return request.param


@pytest.mark.usefixtures("paw_api_client")
class TestConsole:

    def test_list(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.get(f"{self.url}/consoles/")
        self.api.console.list()

    def test_list_shared(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.get(f"{self.url}/consoles/shared_with_you/")
        self.api.console.list_shared()

    def test_create_python3(
        self, mock_responses: 'RequestsMock', params_create: Dict[str, str]
    ) -> None:
        mock_responses.post(
            url=f"{self.url}/consoles/",
            match=(urlencoded_params_matcher({**params_create}), ),
        )
        params_create["executable"] = Python3(params_create["executable"])
        self.api.console.create(**params_create)

    def test_create_bash(
        self, mock_responses: 'RequestsMock', params_create: Dict[str, str]
    ) -> None:
        params_create["executable"] = "bash"
        mock_responses.post(
            url=f"{self.url}/consoles/",
            match=(urlencoded_params_matcher({**params_create}), ),
        )
        params_create["executable"] = Shell(params_create["executable"])
        self.api.console.create(**params_create)

    def test_create_with_args(
        self, mock_responses: 'RequestsMock', params_create: Dict[str, str]
    ) -> None:
        params_create["arguments"] = "--useful-arg"
        mock_responses.post(
            url=f"{self.url}/consoles/",
            match=(urlencoded_params_matcher({**params_create}), ),
        )
        params_create["executable"] = Python3(params_create["executable"])
        self.api.console.create(**params_create)

    def test_info(
        self, mock_responses: 'RequestsMock', console_id: int
    ) -> None:
        mock_responses.get(f"{self.url}/consoles/{console_id}/")
        self.api.console.get_info(console_id)

    def test_kill(
        self, mock_responses: 'RequestsMock', console_id: int
    ) -> None:
        mock_responses.delete(f"{self.url}/consoles/{console_id}/")
        self.api.console.kill(console_id)

    def test_get_output(
        self, mock_responses: 'RequestsMock', console_id: int
    ) -> None:
        mock_responses.get(
            f"{self.url}/consoles/{console_id}/get_latest_output/"
        )
        self.api.console.get_output(console_id)

    def test_send_input(
        self, mock_responses: 'RequestsMock', console_id: int
    ) -> None:
        console_input = "echo 123"
        mock_responses.post(
            url=f"{self.url}/consoles/{console_id}/send_input/",
            match=(urlencoded_params_matcher({"input": console_input}), ),
        )
        self.api.console.send_input(console_id, input_=console_input)
