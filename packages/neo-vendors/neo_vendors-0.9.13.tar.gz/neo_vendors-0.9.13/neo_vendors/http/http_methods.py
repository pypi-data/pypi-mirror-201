from __future__ import annotations

import enum


@enum.unique
class HttpMethodsEnum(str, enum.Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    OPTIONS = 'OPTIONS'
    DELETE = 'DELETE'
    HEAD = 'HEAD'

    def has_request_body_support(self) -> bool:
        cls = self.__class__
        return self in (cls.POST, cls.PUT, cls.PATCH)
