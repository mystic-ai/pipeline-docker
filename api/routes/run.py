import os
import json

from fastapi.routing import APIRouter

from core.middlewares.RouteLogger import RouteLogger

from pipeline.schemas.run import RunGet

router = APIRouter(prefix="/run", route_class=RouteLogger)


@router.post(
    "/",
)
async def create(
    run_data: RunGet,
):
    print("Got run req")

    
    
    return {"": ""}
