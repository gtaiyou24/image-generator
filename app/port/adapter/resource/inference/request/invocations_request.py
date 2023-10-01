import base64
import io

import PIL.Image
import requests
from pydantic import BaseModel, Field


class InvocationsRequest(BaseModel):
    origin: str = Field(title='オリジン画像')
    mask: str = Field(title='マスク画像')
    reference: str = Field(title='リファレンス画像')

    def image(self, name: str) -> PIL.Image.Image:
        if name == 'origin':
            return self.__image_from(self.origin)
        elif name == 'mask':
            return self.__image_from(self.mask)
        else:
            return self.__image_from(self.reference)

    @staticmethod
    def __image_from(source: str) -> PIL.Image.Image:
        if 'base64,' in source:
            image_data = source.split(',')[1]
            image = io.BytesIO(base64.b64decode(image_data))
        else:
            image = requests.get(source, stream=True).raw
        return PIL.Image.open(image).convert("RGB")
