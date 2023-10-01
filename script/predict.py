import argparse
import base64
import io
import json
import os
import zipfile

import PIL
import boto3
import botocore.response
import sagemaker
from sagemaker.predictor import Predictor
from PIL import Image

aws_profile = os.environ.get("AWS_PROFILE")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str)
    parser.add_argument("-n", "--endpoint-name", type=str, required=True)
    args = parser.parse_args()

    boto_session = boto3.Session(profile_name=aws_profile)
    session = sagemaker.Session(boto_session=boto_session)

    predictor = Predictor(
        endpoint_name=args.endpoint_name,
        sagemaker_session=session,
        serializer=sagemaker.serializers.JSONSerializer(),
        deserializer=sagemaker.deserializers.StreamDeserializer(),
    )

    with open(args.input) as jsonfile:
        data = json.load(jsonfile)

    response = predictor.predict(data)
    streaming_body: botocore.response.StreamingBody = response[0]

    zf = zipfile.ZipFile(io.BytesIO(streaming_body.read()), "r")

    for i, fileinfo in enumerate(zf.infolist()):
        image = PIL.Image.open(zf.open(fileinfo.filename))
        print(to_base64(image, image.format.lower()))

        with open(f'./images/{fileinfo.filename}', 'wb') as f:
            f.write(zf.read(fileinfo.filename))


def to_base64(img, format="jpeg"):
    buffer = io.BytesIO()
    img.save(buffer, format)
    img_str = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/{format};base64,{img_str}"


if __name__ == "__main__":
    main()
