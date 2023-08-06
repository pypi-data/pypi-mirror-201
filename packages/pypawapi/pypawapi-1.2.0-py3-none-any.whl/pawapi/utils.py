from .exceptions import InvalidCredentialsError


def validate_credentials(name: str, value: str) -> None:
    if not isinstance(value, str):
        raise InvalidCredentialsError(
            f"{name} must be a str! {name} is {type(value)!r}"
        )
    if value is None or not value:
        raise InvalidCredentialsError(
            f"{name} can't be empty or None! {name} = {value!r}"
        )
    for w in value:
        if w.isspace() or (not w.isalpha() and not w.isdigit()):
            raise InvalidCredentialsError(
                f"{name} has an invalid symbol {w!r}! {name} = {value!r}"
            )
