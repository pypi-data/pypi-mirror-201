from typing import TYPE_CHECKING

import pytest
from responses.matchers import multipart_matcher
from responses.matchers import query_param_matcher
from responses.matchers import urlencoded_params_matcher

if TYPE_CHECKING:
    from responses import RequestsMock

FILE_PATH = "/home/user123/file.md"


@pytest.mark.usefixtures("paw_api_client")
class TestFiles:

    def test_get_file(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.get(f"{self.url}/files/path{FILE_PATH}")
        self.api.file.get_content(FILE_PATH)

    def test_upload_file(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.post(
            url=f"{self.url}/files/path{FILE_PATH}",
            match=(multipart_matcher({"content": b"filecontent"}), ),
        )
        self.api.file.upload(path=FILE_PATH, file_content=b"filecontent")

    def test_delete_file(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.delete(f"{self.url}/files/path{FILE_PATH}")
        self.api.file.delete(FILE_PATH)

    def test_start_sharing_file(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.post(
            url=f"{self.url}/files/sharing/",
            match=(urlencoded_params_matcher({"path": FILE_PATH}), ),
        )
        self.api.file.start_sharing(path=FILE_PATH)

    def test_get_sharing_info(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.get(
            url=f"{self.url}/files/sharing/",
            match=(query_param_matcher({"path": FILE_PATH}), ),
        )
        self.api.file.get_sharing_status(path=FILE_PATH)

    def test_stop_sharing_file(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.delete(
            url=f"{self.url}/files/sharing/",
            match=(query_param_matcher({"path": FILE_PATH}), ),
        )
        self.api.file.stop_sharing(path=FILE_PATH)

    def test_get_contents(self, mock_responses: 'RequestsMock') -> None:
        path = "/home/user/"
        mock_responses.get(
            url=f"{self.url}/files/tree/",
            match=(query_param_matcher({"path": path}), ),
        )
        self.api.file.get_tree(path=path)
