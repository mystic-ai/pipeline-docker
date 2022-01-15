from app.core.exceptions.handlers import get_validation_error_response
from app.services.resource_request import log_request
from pydantic.error_wrappers import ValidationError
from typing import Any, Callable
from fastapi import Request, Response
from fastapi.routing import APIRoute
from starlette.exceptions import HTTPException
from datetime import datetime

from starlette.responses import JSONResponse
from app.database.connections import database_scoped_session
import traceback


class RouteLogger(APIRoute):
    def get_route_handler(self) -> Callable:

        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:

            request_start_time = datetime.now()

            try:
                response: Response = await original_route_handler(request)
            except HTTPException as ex:
                response = JSONResponse(
                    content={"detail": ex.detail},
                    status_code=ex.status_code,
                )
            except ValidationError as ex:
                response = get_validation_error_response(ex)
            except Exception as ex:
                traceback.print_exc()
                response = JSONResponse(
                    content={
                        "detail": "There was an internal error. If this persists please contact support@getneuro.ai"
                    },
                    status_code=500,
                )

            end_time = datetime.now()

            request_duration = int(
                (end_time - request_start_time).total_seconds() * 1000
            )

            await log_request(
                request,
                response.body.decode("utf-8"),
                response.status_code,
                request_start_time,
                request_duration,
            )

            return response

        return custom_route_handler
