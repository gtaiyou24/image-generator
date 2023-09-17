import io
from io import BytesIO
from zipfile import ZipFile

import fastapi
import requests
from PIL import Image
from diffusers import PaintByExamplePipeline
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from port.adapter.resource.inference.request import InvocationsRequest

router = APIRouter(
    prefix='/invocations',
    tags=['推論']
)


@router.post('', name='推論エンドポイント')
def invocations(invocations: InvocationsRequest, request: fastapi.Request):
    init_image = download_image(invocations.image_url).resize((512, 512))
    mask_image = download_image(invocations.mask_url).resize((512, 512))
    example_image = download_image(invocations.example_url).resize((512, 512))

    pipe: PaintByExamplePipeline = request.app.pipe
    images: list[Image.Image] = pipe(image=init_image, mask_image=mask_image, example_image=example_image).images

    zip_buffer = io.BytesIO()
    with ZipFile(zip_buffer, 'w') as zip_file:
        for i, image in enumerate(images):
            memory_stream = io.BytesIO()
            image.save(memory_stream, format="png")
            memory_stream.seek(0)
            zip_file.writestr(f"image_{i}.png", memory_stream.getvalue())

    zip_buffer.seek(0)

    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=images.zip"},
    )


def download_image(url: str) -> Image:
    response = requests.get(url)
    return Image.open(BytesIO(response.content)).convert("RGB")
