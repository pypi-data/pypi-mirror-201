from __future__ import annotations

import traceback
import typing

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from neo_vendors.date_time import utc_now

from ..request_context import RequestIncoming


@typing.runtime_checkable
class IncomingRequestHandler(typing.Protocol):
    async def __call__(self, log_context: RequestIncoming):
        raise NotImplementedError()


class RequestHandlerMiddleware(BaseHTTPMiddleware):
    handler: IncomingRequestHandler
    request_patched: bool = False

    @classmethod
    def patch_request(cls):
        if cls.request_patched:
            return

        stream_original = Request.stream

        async def stream_full(request: Request):
            all_chunks = []
            async for chunk in request.stream():
                all_chunks.append(chunk)
            return b''.join(all_chunks)

        async def stream_patched(request: Request):
            stream_content_key = 'stream_content_key'
            stream_content = request.scope.get(stream_content_key)
            if stream_content is not None:
                yield stream_content
                return
            else:
                stream_content = b''
                async for chunk in stream_original(request):
                    yield chunk
                    stream_content += chunk
                request.scope[stream_content_key] = stream_content
            yield b''

        Request.stream = stream_patched
        Request.stream_full = stream_full
        cls.request_patched = True

    def __init__(self, handler: IncomingRequestHandler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler = handler
        self.patch_request()

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_datetime = utc_now()
        exception_traceback = None
        response = None
        try:
            response = await call_next(request)
            return response
        except Exception:
            exception_traceback = traceback.format_exc()
            raise
        finally:
            response_datetime = utc_now()
            log_context = await RequestIncoming.create(
                request_datetime,
                request,
                response_datetime,
                response=response,
                exception_traceback=exception_traceback,
            )
            await self.handler(log_context)
