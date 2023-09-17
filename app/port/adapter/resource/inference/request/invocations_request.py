from pydantic import BaseModel, Field


class InvocationsRequest(BaseModel):
    image_url: str = Field(title='画像URL')
    mask_url: str = Field(title='マスク画像URL')
    example_url: str = Field(title='参考画像URL')
