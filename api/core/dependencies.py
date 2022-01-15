from core.config import get_settings
from fastapi.security.http import HTTPBearer
from fastapi.security.api_key import APIKeyCookie
from fastapi.params import Depends
from fastapi import Request

from core.config import Settings
from core.exceptions.TokenNotProvided import TokenNotProvided
from core.exceptions.TokenNotFound import TokenNotFound

from typing import Optional

from database.connections import database_scoped_session

bearer_scheme = HTTPBearer(auto_error=False)
cookie_schema = APIKeyCookie(name="token")


async def get_bearer_token(request: Request):
    token_result = await bearer_scheme(request)
    return token_result.credentials if token_result else None


async def get_header_token(
    token: Optional[str] = Depends(get_bearer_token),
    settings: Settings = Depends(get_settings),
):
    if not token:
        raise TokenNotProvided()

    database_token = (
        database_scoped_session.query(Token).filter(Token.token == token).first()
    )

    if not database_token and token != settings.PIPELINE_TOKEN:
        raise TokenNotFound(token=token)

    return token


async def get_cookie_token(
    cookie_token: Optional[str] = Depends(cookie_schema),
    header_token: Optional[str] = Depends(get_header_token),
):
    if cookie_token != header_token:
        raise TokenNotFound(token=cookie_token, message="Token clash")
    return cookie_token
