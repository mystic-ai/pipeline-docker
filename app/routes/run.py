import os
import json

from dill import loads

from os import listdir
from os.path import isfile, join

from fastapi.routing import APIRouter

from app.core.middlewares.RouteLogger import RouteLogger

from pipeline.schemas.run import RunGet
from pipeline.objects import Graph

router = APIRouter(prefix="/run", route_class=RouteLogger)


pipeline_graph_files = [f for f in listdir("/app/pipelines") if isfile(join("/app/pipelines", f)) and f.endswith(".graph")]
for file_str in pipeline_graph_files:
    with open(join("/app/pipelines/", file_str), "rb") as pipeline_graph_file:
        pipeline_graph = loads(pipeline_graph_file.read())
        if isinstance(pipeline_graph, Graph):

            #expected_inputs = pipeline_graph.inputs

            @router.post(
                "/%s" % pipeline_graph.name,
            )
            async def create(
                pipeline_inputs: dict,
            ):
                print("Got run req")
                return {"result":pipeline_graph.run(pipeline_inputs)}