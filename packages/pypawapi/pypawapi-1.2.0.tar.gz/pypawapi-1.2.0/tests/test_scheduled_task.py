from typing import TYPE_CHECKING
from typing import Any
from typing import Dict

import pytest
from responses.matchers import urlencoded_params_matcher

from pawapi.interval import TaskInterval

if TYPE_CHECKING:
    from responses import RequestsMock


@pytest.fixture
def params_create_hourly() -> Dict[str, Any]:
    return {
        "command": "echo 123 >> file",
        "enabled": True,
        "interval": "hourly",
        "minute": 12,
        "description": "Schedule hourly description",
    }


@pytest.fixture
def params_create_daily(params_create_hourly: Dict[str, Any]) -> Dict[str, Any]:
    params_create_hourly.update({
        "hour": 12,
        "interval": "daily",
        "description": "Schedule daily description",
    })
    return params_create_hourly


def test_schedule_interval() -> None:
    assert TaskInterval.DAILY.value == "daily"
    assert TaskInterval.HOURLY.value == "hourly"


TASK_ID = 12


@pytest.mark.usefixtures("paw_api_client")
class TestScheduledTask:

    def test_list(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.get(f"{self.url}/schedule/")
        self.api.scheduled_task.list()

    def test_create_hourly(
        self,
        mock_responses: 'RequestsMock',
        params_create_hourly: Dict[str, Any],
    ) -> None:
        mock_responses.post(
            url=f"{self.url}/schedule/",
            match=(
                urlencoded_params_matcher({
                    k: str(v)
                    for k, v in params_create_hourly.items()
                }),
            ),
        )
        params_create_hourly["interval"] = TaskInterval.HOURLY
        self.api.scheduled_task.create(**params_create_hourly)

    def test_create_daily(
        self,
        mock_responses: 'RequestsMock',
        params_create_daily: Dict[str, Any],
    ) -> None:
        mock_responses.post(
            url=f"{self.url}/schedule/",
            match=(
                urlencoded_params_matcher({
                    k: str(v)
                    for k, v in params_create_daily.items()
                }),
            ),
        )
        params_create_daily["interval"] = TaskInterval.DAILY
        self.api.scheduled_task.create(**params_create_daily)

    def test_info(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.get(f"{self.url}/schedule/{TASK_ID}/")
        self.api.scheduled_task.get_info(TASK_ID)

    def test_update_full(
        self,
        mock_responses: 'RequestsMock',
        params_create_daily: Dict[str, Any],
    ) -> None:
        params_create_daily.update({
            "hour": 21,
            "minute": 21,
            "description": "Updated description",
        })
        mock_responses.patch(
            url=f"{self.url}/schedule/{TASK_ID}/",
            match=(
                urlencoded_params_matcher({
                    k: str(v)
                    for k, v in params_create_daily.items()
                }),
            ),
        )
        params_create_daily["interval"] = TaskInterval(
            params_create_daily["interval"]
        )
        self.api.scheduled_task.update(
            task_id=TASK_ID,
            **params_create_daily,
        )

    def test_update_time(self, mock_responses: 'RequestsMock') -> None:
        params = {"hour": 12, "minute": 12}
        mock_responses.patch(
            url=f"{self.url}/schedule/{TASK_ID}/",
            match=(
                urlencoded_params_matcher({
                    k: str(v)
                    for k, v in params.items()
                }),
            ),
        )
        self.api.scheduled_task.update(task_id=TASK_ID, **params)

    def test_delete(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.delete(f"{self.url}/schedule/{TASK_ID}/")
        self.api.scheduled_task.delete(TASK_ID)
