from __future__ import annotations

import typing

from . import base


class ApiException(Exception):
    status_code: int
    api_error: base.ApiError

    def __init__(
            self,
            status_code: int,
            code: str,
            message: typing.Optional[str] = None,
            payload: typing.Optional[typing.Any] = None,
    ):
        self.status_code = status_code
        self.api_error = base.ApiError(
            code=code,
            message=message,
            payload=payload,
        )
