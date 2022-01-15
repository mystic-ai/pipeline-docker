from app.services.resource_request import log_request
from datetime import datetime
from fastapi.exception_handlers import (
    http_exception_handler,
)
from fastapi.exceptions import HTTPException
from pydantic.error_wrappers import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


async def validation_exception_handler(request: Request, exc: ValidationError):

    response = get_validation_error_response(exc)

    await log_request(request, response.body.decode("utf-8"), 422, datetime.now(), 0)

    return get_validation_error_response(exc)


async def http_exception_handler(request: Request, exc: HTTPException):
    await log_request(
        request,
        str({"detail": exc.detail}),
        exc.status_code,
        datetime.now(),
        0,
    )
    return await http_exception_handler(request, exc)


def get_validation_error_response(exc: ValidationError):
    errors = exc.errors()
    response = JSONResponse(
        content={
            "detail": {
                "message": f"{len(errors)} validation errors in request",
                "errors": [
                    {
                        "parameter": "->".join(
                            [str(location) for location in error["loc"]]
                        ),
                        "error": error["msg"],
                    }
                    for error in errors
                ],
            }
        },
        status_code=422,
    )

    return response
