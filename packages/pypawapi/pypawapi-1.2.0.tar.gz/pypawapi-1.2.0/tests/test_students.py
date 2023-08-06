from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from responses import RequestsMock


@pytest.mark.usefixtures("paw_api_client")
class TestStudents:

    def test_list(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.get(f"{self.url}/students/")
        self.api.students.list()

    @pytest.mark.parametrize("student", ("student1", "anotherstudent2"))
    def test_delete(self, mock_responses: 'RequestsMock', student: str) -> None:
        mock_responses.delete(f"{self.url}/students/{student}/")
        self.api.students.delete(student)
