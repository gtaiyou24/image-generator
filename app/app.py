import os
from contextlib import asynccontextmanager

import torch
from diffusers import DiffusionPipeline
from fastapi import FastAPI

from port.adapter.resource.inference import inference_resource
from port.adapter.resource.ping import ping_resource


@asynccontextmanager
async def lifespan(app: FastAPI):
    pipe = DiffusionPipeline.from_pretrained(
        "Fantasy-Studio/Paint-by-Example",
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
    )
    pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")
    app.pipe = pipe
    yield
    app.clip = None


app = FastAPI(title="Image Generator", openapi_prefix=os.getenv('OPENAPI_PREFIX'), lifespan=lifespan)
app.include_router(inference_resource.router)
app.include_router(ping_resource.router)
