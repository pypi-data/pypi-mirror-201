__all__ = ["File"]

from pawapi.response import Response

from .base import BaseEndpoint


class File(BaseEndpoint):
    __endpoint = "files"

    __slots__ = ()

    def get_content(self, path: str) -> Response:
        """ Get content of file or directory file list """

        return self._client.get(f"{self.__endpoint}/path{path}")

    def upload(self, path: str, file_content: bytes) -> Response:
        """ Uploads a file to the specified file path """

        return self._client.post(
            path=f"{self.__endpoint}/path{path}",
            files={"content": file_content},
        )

    def delete(self, path: str) -> Response:
        """ Deletes the file at the specified path """

        return self._client.delete(f"{self.__endpoint}/path{path}")

    def start_sharing(self, path: str) -> Response:
        """ Start sharing a file """

        return self._client.post(
            path=f"{self.__endpoint}/sharing/",
            data={"path": path},
        )

    def get_sharing_status(self, path: str) -> Response:
        """ Sharing status for a path """

        return self._client.get(f"{self.__endpoint}/sharing/", {"path": path})

    def stop_sharing(self, path: str) -> Response:
        """ Stop sharing a path """

        return self._client.delete(
            path=f"{self.__endpoint}/sharing/",
            params={"path": path},
        )

    def get_tree(self, path: str) -> Response:
        """ Returns a list of the contents of a directory,
            and its subdirectories as a list. Paths ending
            in slash/ represent directories.

            NOTE: max 1000 results
        """

        return self._client.get(f"{self.__endpoint}/tree/", {"path": path})
