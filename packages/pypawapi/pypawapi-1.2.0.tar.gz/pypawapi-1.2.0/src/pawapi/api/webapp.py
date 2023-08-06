__all__ = ["Webapp"]

from typing import Optional
from typing import Union

from pawapi.python import Python2
from pawapi.python import Python3
from pawapi.response import Response

from .base import BaseEndpoint


class Webapp(BaseEndpoint):
    __endpoint = "webapps"

    __slots__ = ()

    def list(self) -> Response:
        """ List all webapps """

        return self._client.get(f"{self.__endpoint}/")

    def create(
        self,
        domain_name: str,
        python_version: Union[Python2, Python3],
    ) -> Response:
        """ Create a new webapp with manual configuration """

        return self._client.post(
            path="webapps/",
            data={
                "domain_name": domain_name,
                "python_version": python_version.format_value(dot=False),
            },
        )

    def get_info(self, domain_name: str) -> Response:
        """ Information about a web app's configuration """

        return self._client.get(f"{self.__endpoint}/{domain_name}/")

    def update(
        self,
        domain_name: str,
        *,
        python_version: Optional[Union[Python2, Python3]] = None,
        source_directory: Optional[str] = None,
        virtualenv_path: Optional[str] = None,
        force_https: Optional[bool] = None,
        protection: Optional[bool] = None,
        protection_username: Optional[str] = None,
        protection_password: Optional[str] = None,
    ) -> Response:
        """ Modify configuration of a webapp

            NOTE: restart the webapp is required to apply the changes
        """

        pyver = None
        if python_version is not None:
            pyver = python_version.format_value(short=True)

        return self._client.patch(
            path=f"{self.__endpoint}/{domain_name}/",
            data={
                "python_version": pyver,
                "source_directory": source_directory,
                "virtualenv_path": virtualenv_path,
                "force_https": force_https,
                "password_protection_enabled": protection,
                "password_protection_username": protection_username,
                "password_protection_password": protection_password,
            },
        )

    def delete(self, domain_name: str) -> Response:
        """ Delete the webapp

            NOTE: Config is backed up in /var/www, and your code is not touched
        """

        return self._client.delete(f"{self.__endpoint}/{domain_name}/")

    def enable(self, domain_name: str) -> Response:
        """ Enable the webapp """

        return self._client.post(f"{self.__endpoint}/{domain_name}/enable/")

    def disable(self, domain_name: str) -> Response:
        """ Disable the webapp """

        return self._client.post(f"{self.__endpoint}/{domain_name}/disable/")

    def reload(self, domain_name: str) -> Response:
        """ Reload the webapp """

        return self._client.post(f"{self.__endpoint}/{domain_name}/reload/")

    def get_ssl_info(self, domain_name: str) -> Response:
        """ Information about webapp's SSL """

        return self._client.get(f"{self.__endpoint}/{domain_name}/ssl/")

    def add_ssl(
        self,
        domain_name: str,
        cert: str,
        private_key: str,
    ) -> Response:
        """ Set SSL cert for webapp """

        return self._client.post(
            path=f"{self.__endpoint}/{domain_name}/ssl/",
            data={
                "cert": cert,
                "private_key": private_key,
            },
        )

    def delete_ssl(self, domain_name: str) -> Response:
        """ Delete webapp's SSL """

        return self._client.delete(f"{self.__endpoint}/{domain_name}/ssl/")

    def list_static_files(self, domain_name: str) -> Response:
        """ List all the static files mappings for a domain """

        return self._client.get(
            f"{self.__endpoint}/{domain_name}/static_files/"
        )

    def add_static_file(
        self,
        domain_name: str,
        url: str,
        path: str,
    ) -> Response:
        """ Create a new static files mapping

            NOTE: webapp restart required
        """

        return self._client.post(
            path=f"{self.__endpoint}/{domain_name}/static_files/",
            data={
                "url": url,
                "path": path,
            },
        )

    def get_static_file_info(self, domain_name: str, file_id: int) -> Response:
        """ URL and path of a particular mapping """

        return self._client.get(
            f"{self.__endpoint}/{domain_name}/static_files/{file_id}/"
        )

    def update_static_file(
        self,
        domain_name: str,
        file_id: int,
        url: str,
        path: str,
    ) -> Response:
        """ Modify a static files mapping

            NOTE: webapp restart required
        """

        return self._client.patch(
            path=f"{self.__endpoint}/{domain_name}/static_files/{file_id}/",
            data={
                "url": url,
                "path": path,
            },
        )

    def delete_static_file(self, domain_name: str, file_id: int) -> Response:
        """ Remove a static files mapping

            NOTE: webapp restart required
        """

        return self._client.delete(
            f"{self.__endpoint}/{domain_name}/static_files/{file_id}/"
        )

    def list_static_headers(self, domain_name: str) -> Response:
        """ List all the static headers for a domain """

        return self._client.get(
            f"{self.__endpoint}/{domain_name}/static_headers/"
        )

    def add_static_header(
        self,
        domain_name: str,
        url: str,
        name: str,
        value: str,
    ) -> Response:
        """ Create a new static header

            NOTE: webapp restart required
        """

        return self._client.post(
            path=f"{self.__endpoint}/{domain_name}/static_headers/",
            data={
                "url": url,
                "name": name,
                "value": value,
            },
        )

    def get_static_header_info(
        self,
        domain_name: str,
        header_id: int,
    ) -> Response:
        """ URL, name and value of a particular header """

        return self._client.get(
            f"{self.__endpoint}/{domain_name}/static_headers/{header_id}/"
        )

    def update_static_header(
        self,
        domain_name: str,
        header_id: int,
        url: str,
        name: str,
        value: str,
    ) -> Response:
        """ Modify a static header

            NOTE: webapp restart required
        """

        return self._client.patch(
            path=f"{self.__endpoint}/{domain_name}/static_headers/{header_id}/",
            data={
                "url": url,
                "name": name,
                "value": value,
            },
        )

    def delete_static_header(
        self,
        domain_name: str,
        header_id: int,
    ) -> Response:
        """ Remove a static header

            NOTE: webapp restart required
        """

        return self._client.delete(
            f"{self.__endpoint}/{domain_name}/static_headers/{header_id}/"
        )
