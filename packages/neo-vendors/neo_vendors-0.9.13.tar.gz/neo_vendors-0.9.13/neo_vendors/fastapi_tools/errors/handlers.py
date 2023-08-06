from __future__ import annotations

from fastapi import Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status


from . import exceptions
from . import payloads


def api_error_exception_handler(_: Request, exc: exceptions.ApiException) -> Response:
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(exc.api_error),
    )


def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> Response:
    request_validation_error_code = "request_validation_error"
    errors = []
    for error in exc.raw_errors:
        if hasattr(error.exc, 'raw_errors'):  # type: ignore
            first_error = error.exc.raw_errors[0]  # type: ignore
            message = str(first_error.exc)
            field = first_error._loc
        else:
            first_error = error
            message = str(first_error.exc)
            field = first_error._loc[0]
        payload = payloads.ValidationErrorPayload(
            field=field,
            message=message,
        )
        errors.append(payload)
    request_validation_exception = exceptions.ApiException(
        status.HTTP_400_BAD_REQUEST,
        request_validation_error_code,
        payload=errors[0] if errors else None,
    )
    return api_error_exception_handler(request, request_validation_exception)
