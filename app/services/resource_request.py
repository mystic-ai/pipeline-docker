from app.core.dependencies import get_bearer_token
from app.core.config import get_settings
from datetime import datetime
from typing import Any
from starlette.requests import Request
from app.core.exceptions.PermissionNotGranted import PermissionNotGranted

from app.database.connections import database_scoped_session
from app.core.exceptions.InvalidParameter import InvalidParameter
from app.core.exceptions.RequestFailed import RequestFailed
from app.database.models import ResourceRequest


def get_resource_request_info(request_id: str, token: str):

    # TODO: Add permissions

    resource_request = (
        database_scoped_session.query(ResourceRequest)
        .filter(ResourceRequest.id == request_id)
        .first()
    )

    if not resource_request:
        raise RequestFailed(message="Request does not exist")

    return resource_request.as_dict()


def get_request_list(token_value: str):

    requests = database_scoped_session.query(ResourceRequest).all()

    formatted_requests = [req.as_dict() for req in requests]

    return formatted_requests


async def log_request(
    request: Request,
    response_body: str,
    status_code: int,
    req_time: datetime,
    req_duration: int,
):

    settings = get_settings()

    token = await get_bearer_token(request)

    request_ip = request.client.host
    if request.headers.getlist("X-Forwarded-For"):
        request_ip = request.headers.getlist("X-Forwarded-For")[0]

    request_body = (await request.body()).decode("utf-8")
    request_url = request.url.path
    request_method = request.method

    result_json = (
        response_body if len(response_body) < 10240 else response_body[:10237] + "..."
    )
    request_status = status_code

    resource_request_entry = ResourceRequest(
        token=token,
        status=request_status,
        request_json=request_body,
        result_json=result_json,
        result_file_url="",
        resource_url=request_url,
        request_method=request_method,
        time_requested=req_time,
        request_duration=req_duration,
        ip_address=request_ip,
    )

    database_scoped_session.add(resource_request_entry)
    database_scoped_session.commit()