from __future__ import annotations

import typing

import pydantic


class ApiError(pydantic.BaseModel):
    code: str
    message: typing.Optional[str] = None
    payload: typing.Optional[typing.Any] = None
