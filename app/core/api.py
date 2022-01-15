import json

from pydantic.error_wrappers import ValidationError
from app.core.exceptions.handlers import (
    validation_exception_handler,
    http_exception_handler,
)
from fastapi.exceptions import HTTPException
from app.core.middlewares.RouteLogger import RouteLogger
from fastapi.routing import APIRouter
from fastapi import FastAPI
import logging

from app.routes.run import router as run_router

app = FastAPI()
logger = logging.getLogger("uvicorn")

main_router = APIRouter(prefix="/v2", route_class=RouteLogger)
main_router.include_router(run_router)


@main_router.get("/status")
async def status():
    return {"alive": True}


app.include_router(main_router)


app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
