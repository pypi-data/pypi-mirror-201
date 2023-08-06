from __future__ import annotations

import asyncio
import datetime
import http
import traceback
import types
import typing
import urllib.parse

import aiohttp
from aiohttp.helpers import sentinel

from neo_vendors.date_time import utc_now
from neo_vendors.http import http_methods
from neo_vendors.http import request_context


class AsyncHttpProviderException(Exception):
    pass


class AsyncHttpProviderRequestException(AsyncHttpProviderException):
    pass


class AsyncHttpProviderNot2XXException(AsyncHttpProviderException):
    status_code: int
    content: bytes

    def __init__(self, status_code: int, content: bytes):
        self.status_code = status_code
        self.content = content


class AsyncHttpProvider:
    base_url: str
    timeout: typing.Optional[datetime.timedelta]
    proxy: typing.Optional[str]
    headers: typing.Optional[typing.Dict[str, str]]
    cookies: typing.Optional[typing.Dict[str, str]]
    trace_configs: typing.Optional[typing.List[aiohttp.TraceConfig]]
    session: typing.Optional[aiohttp.ClientSession]

    def __init__(
            self,
            *,
            base_url: str,
            timeout: typing.Optional[datetime.timedelta] = None,
            headers: typing.Optional[typing.Dict[str, str]] = None,
            cookies: typing.Optional[typing.Dict[str, str]] = None,
            proxy: typing.Optional[str] = None,
            trace_configs: typing.Optional[typing.List[aiohttp.TraceConfig]] = None,
    ):
        self.base_url = base_url
        self.timeout = timeout
        self.headers = headers
        self.cookies = cookies
        self.proxy = proxy
        self.trace_configs = trace_configs
        self.session = None

    async def __aenter__(self) -> typing.Self:
        session = self.create_session()
        if session.closed:
            raise TypeError("session is closed")
        self.session = session
        return self

    async def __aexit__(
            self,
            exc_type: typing.Type[BaseException],
            exc_val: BaseException,
            exc_tb: types.TracebackType,
    ):
        if self.session is not None and not self.session.closed:
            await self.session.close()
        self.session = None

    def create_session(self) -> aiohttp.ClientSession:
        connector = self.create_connector()
        session = aiohttp.ClientSession(
            connector=connector,
            headers=self.headers,
            cookies=self.cookies,
            timeout=aiohttp.ClientTimeout(self.timeout.total_seconds()) if self.timeout is not None else sentinel,
            trace_configs=self.trace_configs,
        )
        return session

    @staticmethod
    def create_connector() -> aiohttp.BaseConnector:
        connector = aiohttp.TCPConnector(
            limit=0,
            limit_per_host=0,
            force_close=True,
            enable_cleanup_closed=True,
            verify_ssl=True,
        )
        return connector

    async def make_http(
            self,
            *,
            path: str,
            method: http_methods.HttpMethodsEnum,
            query_params: typing.Optional[typing.Dict[str, str]] = None,
            request_body: typing.Optional[bytes] = None,
            max_tries: int = 1,
            relax_time: typing.Optional[datetime.timedelta] = None,
    ) -> bytes:
        if self.session is None:
            raise TypeError("session is None")
        if self.session.closed:
            raise TypeError("session is closed")
        if request_body is not None and not method.has_request_body_support():
            raise ValueError(f"request body is not supported for http method = {method.value}")
        http_invoker = self.get_invoker(method)
        full_url = urllib.parse.urljoin(self.base_url, path)
        relax_time = relax_time or datetime.timedelta(seconds=5)
        try_count = 0
        while True:
            try_count += 1
            try:
                try:
                    response = await http_invoker(
                        full_url,
                        allow_redirects=True,
                        data=request_body,
                        params=query_params,
                        proxy=f"http://{self.proxy}" if self.proxy is not None else None,
                    )
                    break
                except (
                    ConnectionResetError,
                    asyncio.exceptions.TimeoutError,
                    aiohttp.ClientError,
                ) as exc:
                    raise AsyncHttpProviderRequestException() from exc
            except AsyncHttpProviderRequestException:
                if max_tries <= try_count:
                    raise
                await asyncio.sleep(relax_time.total_seconds())
        try:
            content: bytes = await response.read()
            status = response.status
            if not (http.HTTPStatus.OK <= status < http.HTTPStatus.MULTIPLE_CHOICES):
                raise AsyncHttpProviderNot2XXException(status, content)
            return content
        finally:
            response.close()

    def get_invoker(self, method: http_methods.HttpMethodsEnum) -> typing.Callable:
        if self.session is None:
            raise Exception('session is None')
        http_methods_map = {
            http_methods.HttpMethodsEnum.GET: self.session.get,
            http_methods.HttpMethodsEnum.POST: self.session.post,
            http_methods.HttpMethodsEnum.PUT: self.session.put,
            http_methods.HttpMethodsEnum.PATCH: self.session.patch,
            http_methods.HttpMethodsEnum.DELETE: self.session.delete,
            http_methods.HttpMethodsEnum.HEAD: self.session.head,
        }
        return typing.cast(typing.Callable, http_methods_map[method])

    async def make_get(
            self,
            *,
            path: str,
            query_params: typing.Optional[typing.Dict[str, str]] = None,
            max_tries: int = 1,
            relax_time: typing.Optional[datetime.timedelta] = None,
    ) -> bytes:
        return await self.make_http(
            path=path,
            method=http_methods.HttpMethodsEnum.GET,
            query_params=query_params,
            request_body=None,
            max_tries=max_tries,
            relax_time=relax_time,
        )

    async def make_post(
            self,
            *,
            path: str,
            query_params: typing.Optional[typing.Dict[str, str]] = None,
            request_body: typing.Optional[bytes] = None,
            max_tries: int = 1,
            relax_time: typing.Optional[datetime.timedelta] = None,
    ) -> bytes:
        return await self.make_http(
            path=path,
            method=http_methods.HttpMethodsEnum.POST,
            query_params=query_params,
            request_body=request_body,
            max_tries=max_tries,
            relax_time=relax_time,
        )


class RequestContextWrapper(types.SimpleNamespace):
    context: request_context.RequestOutgoing

    def __init__(self, trace_request_ctx: typing.Optional[types.SimpleNamespace] = None):
        self.context = request_context.RequestOutgoing()
        super(RequestContextWrapper, self).__init__()


class AsyncRequestContexHandleTraceConfig(aiohttp.TraceConfig):
    request_outgoing_handler: request_context.RequestOutgoingHandlerProtocolAsync

    def __init__(
            self,
            request_outgoing_handler: request_context.RequestOutgoingHandlerProtocolAsync,
    ):
        super().__init__(trace_config_ctx_factory=RequestContextWrapper)
        self.request_outgoing_handler = request_outgoing_handler
        self.on_request_start.append(self.on_request_start_handler)  # type: ignore
        self.on_request_chunk_sent.append(self.on_request_chunk_sent_handler)  # type: ignore
        self.on_request_end.append(self.on_request_end_handler)  # type: ignore
        self.on_request_exception.append(self.on_request_exception_handler)  # type: ignore

    @staticmethod
    async def on_request_start_handler(
            session: aiohttp.ClientSession,
            trace_config_ctx: RequestContextWrapper,
            start_params: aiohttp.TraceRequestStartParams,
    ):
        trace_config_ctx.context.request_datetime = utc_now()
        trace_config_ctx.context.request_url = str(start_params.url)
        trace_config_ctx.context.request_method = start_params.method
        trace_config_ctx.context.request_headers = {}
        for k, v in start_params.headers.items():
            trace_config_ctx.context.request_headers[k] = v

    @staticmethod
    async def on_request_chunk_sent_handler(
            session: aiohttp.ClientSession,
            trace_config_ctx: RequestContextWrapper,
            params: aiohttp.TraceRequestChunkSentParams,
    ):
        trace_config_ctx.context.request_body = params.chunk

    async def on_request_end_handler(
            self,
            session: aiohttp.ClientSession,
            trace_config_ctx: RequestContextWrapper,
            params: aiohttp.TraceRequestEndParams,
    ):
        if trace_config_ctx.context.request_datetime is None:
            raise ValueError("trace_config_ctx.context.request_datetime is None")
        assert trace_config_ctx.context.request_datetime is not None
        trace_config_ctx.context.response_datetime = utc_now()
        trace_config_ctx.context.elapsed_time = (
                trace_config_ctx.context.response_datetime - trace_config_ctx.context.request_datetime
        )
        trace_config_ctx.context.response_status_code = params.response.status
        trace_config_ctx.context.response_body = await params.response.read()
        trace_config_ctx.context.response_headers = {}
        for k, v in params.headers.items():
            trace_config_ctx.context.response_headers[k] = v
        trace_config_ctx.context.exception = None
        await self.request_outgoing_handler(trace_config_ctx.context)

    async def on_request_exception_handler(
            self,
            session: aiohttp.ClientSession,
            trace_config_ctx: RequestContextWrapper,
            params: aiohttp.TraceRequestExceptionParams,
    ):
        if trace_config_ctx.context.request_datetime is None:
            raise ValueError("trace_config_ctx.context.request_datetime is None")
        trace_config_ctx.context.response_datetime = utc_now()
        trace_config_ctx.context.elapsed_time = (
                trace_config_ctx.context.response_datetime - trace_config_ctx.context.request_datetime
        )
        trace_config_ctx.context.response_status_code = None
        trace_config_ctx.context.response_body = None
        trace_config_ctx.context.response_headers = None
        trace_config_ctx.context.exception = ''.join(traceback.format_tb(params.exception.__traceback__))
        await self.request_outgoing_handler(trace_config_ctx.context)
