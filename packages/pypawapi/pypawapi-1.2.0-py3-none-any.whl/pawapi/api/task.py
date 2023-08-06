__all__ = [
    "ScheduledTask",
    "AlwaysOnTask",
]

from typing import Optional
from typing import Union

from pawapi.interval import TaskInterval
from pawapi.response import Response

from .base import BaseEndpoint


class ScheduledTask(BaseEndpoint):
    __endpoint = "schedule"

    __slots__ = ()

    def list(self) -> Response:
        """ List all tasks """

        return self._client.get(f"{self.__endpoint}/")

    def create(
        self,
        command: str,
        minute: Union[int, str],
        *,
        hour: Optional[Union[int, str]] = None,
        enabled: bool = True,
        interval: TaskInterval = TaskInterval.DAILY,
        description: Optional[str] = None,
    ) -> Response:
        """ Create a new task """

        return self._client.post(
            path=f"{self.__endpoint}/",
            data={
                "command": command,
                "enabled": enabled,
                "interval": interval.value,
                "hour": hour,
                "minute": minute,
                "description": description,
            },
        )

    def get_info(self, task_id: Union[int, str]) -> Response:
        """ Information about task """

        return self._client.get(f"{self.__endpoint}/{task_id}/")

    def update(
        self,
        task_id: Union[int, str],
        *,
        command: Optional[str] = None,
        enabled: Optional[bool] = None,
        interval: Optional[TaskInterval] = None,
        hour: Optional[Union[int, str]] = None,
        minute: Optional[Union[int, str]] = None,
        description: Optional[str] = None,
    ) -> Response:
        """ Update task """

        return self._client.patch(
            path=f"{self.__endpoint}/{task_id}/",
            data={
                "command": command,
                "enabled": enabled,
                "interval": interval.value if interval is not None else None,
                "hour": hour,
                "minute": minute,
                "description": description,
            },
        )

    def delete(self, task_id: Union[int, str]) -> Response:
        """ Stop and delete task """

        return self._client.delete(f"{self.__endpoint}/{task_id}/")


class AlwaysOnTask(BaseEndpoint):
    _endpoint = "always_on"

    __slots__ = ()

    def list(self) -> Response:
        """ List all tasks """

        return self._client.get(f"{self._endpoint}/")

    def create(
        self,
        command: str,
        *,
        enabled: bool = True,
        description: Optional[str] = None,
    ) -> Response:
        """ Create a new task """

        return self._client.post(
            path=f"{self._endpoint}/",
            data={
                "command": command,
                "description": description,
                "enabled": enabled,
            },
        )

    def get_info(self, task_id: Union[int, str]) -> Response:
        """ Information about task """

        return self._client.get(f"{self._endpoint}/{task_id}/")

    def update(
        self,
        task_id: Union[int, str],
        *,
        command: Optional[str] = None,
        description: Optional[str] = None,
        enabled: Optional[bool] = None,
    ) -> Response:
        """ Modify configuration of task """

        return self._client.patch(
            path=f"{self._endpoint}/{task_id}/",
            data={
                "command": command,
                "description": description,
                "enabled": enabled,
            },
        )

    def delete(self, task_id: Union[int, str]) -> Response:
        """ Stop and delete task """

        return self._client.delete(f"{self._endpoint}/{task_id}/")

    def restart(
        self,
        task_id: Union[int, str],
        *,
        command: Optional[str] = None,
        description: Optional[str] = None,
        enabled: Optional[bool] = None,
    ) -> Response:
        """ Restart task """

        return self._client.post(
            path=f"{self._endpoint}/{task_id}/restart/",
            data={
                "command": command,
                "description": description,
                "enabled": enabled,
            },
        )
