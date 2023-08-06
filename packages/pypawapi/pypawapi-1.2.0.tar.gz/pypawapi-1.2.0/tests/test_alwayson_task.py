from typing import TYPE_CHECKING
from typing import Any
from typing import Dict

import pytest
from responses.matchers import urlencoded_params_matcher

if TYPE_CHECKING:
    from responses import RequestsMock


@pytest.fixture
def params_create() -> Dict[str, Any]:
    return {
        "command": "bash script.sh",
        "description": "Magic bash script",
        "enabled": True,
    }


@pytest.fixture
def params_update(params_create: Dict[str, Any]) -> Dict[str, Any]:
    params_create.update({
        "command": "python script.py",
        "description": "Magic python script",
    })
    return params_create


@pytest.mark.usefixtures("paw_api_client")
class TestAlwaysOnTask:
    task_id = 12

    def test_list(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.get(f"{self.url}/always_on/")
        self.api.alwayson_task.list()

    def test_create(
        self, mock_responses: 'RequestsMock', params_create: Dict[str, Any]
    ) -> None:
        mock_responses.post(
            url=f"{self.url}/always_on/",
            match=(
                urlencoded_params_matcher({
                    k: str(v)
                    for k, v in params_create.items()
                }),
            ),
        )
        self.api.alwayson_task.create(**params_create)

    def test_info(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.get(f"{self.url}/always_on/{self.task_id}/")
        self.api.alwayson_task.get_info(self.task_id)

    def test_update(
        self,
        mock_responses: 'RequestsMock',
        params_update: Dict[str, Any],
    ) -> None:
        mock_responses.patch(
            url=f"{self.url}/always_on/{self.task_id}/",
            match=(
                urlencoded_params_matcher({
                    k: str(v)
                    for k, v in params_update.items()
                }),
            ),
        )
        self.api.alwayson_task.update(task_id=self.task_id, **params_update)

    def test_delete(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.delete(f"{self.url}/always_on/{self.task_id}/")
        self.api.alwayson_task.delete(self.task_id)

    def test_restart(
        self,
        mock_responses: 'RequestsMock',
        params_update: Dict[str, Any],
    ) -> None:
        mock_responses.post(
            url=f"{self.url}/always_on/{self.task_id}/restart/",
            match=(
                urlencoded_params_matcher({
                    k: str(v)
                    for k, v in params_update.items()
                }),
            ),
        )
        self.api.alwayson_task.restart(task_id=self.task_id, **params_update)
