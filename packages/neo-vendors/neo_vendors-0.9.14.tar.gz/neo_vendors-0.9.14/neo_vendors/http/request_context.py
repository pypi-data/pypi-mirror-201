from __future__ import annotations

import datetime
import dataclasses
import typing
import types


@dataclasses.dataclass
class RequestOutgoing(types.SimpleNamespace):
    request_datetime: typing.Optional[datetime.datetime] = None
    request_url: typing.Optional[str] = None
    request_method: typing.Optional[str] = None
    request_headers: typing.Optional[typing.Dict[str, str]] = None
    request_body: typing.Optional[bytes] = None

    response_datetime: typing.Optional[datetime.datetime] = None
    response_status_code: typing.Optional[int] = None
    response_headers: typing.Optional[typing.Dict[str, str]] = None
    response_body: typing.Optional[bytes] = None

    elapsed_time: typing.Optional[datetime.timedelta] = None
    exception: typing.Optional[str] = None
    proxy: typing.Optional[str] = None


class RequestOutgoingHandlerProtocol(typing.Protocol):
    def __call__(self, request_context: RequestOutgoing):
        pass


class RequestOutgoingHandlerProtocolAsync(typing.Protocol):
    async def __call__(self, request_context: RequestOutgoing):
        pass
