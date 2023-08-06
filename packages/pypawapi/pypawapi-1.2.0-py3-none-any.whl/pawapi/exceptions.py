from typing import Optional


class PythonAnywhereAPIException(Exception):
    """ Base server side exception """

    def __init__(
        self,
        status_code: int,
        description: Optional[str] = None,
        raw_content: Optional[bytes] = None,
    ) -> None:
        message = str(status_code)
        if description:
            message = f"{message}, {description}"
        super().__init__(message)
        self.status_code = status_code
        self.description = description
        self.raw_content = raw_content

    def __reduce__(self):  # pragma: no cover
        return (
            self.__class__,
            (
                self.status_code,
                self.description,
                self.raw_content,
            ),
        )


class InvalidTokenError(PythonAnywhereAPIException):
    """ Invalid API token (status code 401) """


class PermissionDeniedError(PythonAnywhereAPIException):
    """ Wrong username or somthing else (status code 403) """


class NotFoundError(PythonAnywhereAPIException):
    """ Path not found (status code 404) """


class StatusError(PythonAnywhereAPIException):
    """ Status code >= 400 (except 401, 403, 404) """


class PawapiException(Exception):
    """ Base client side exception """


class InvalidJSONError(PawapiException):
    """ Error while parsing json response """


class InvalidCredentialsError(PawapiException):
    """ Username or Token has an invalid character """


class RequestTimeoutError(PawapiException):
    """ Request timed out """
