# Image Generator

## How To

<details><summary>setup Lightsail</summary>

```bash
docker build -t image-generator:lightsail . -f ./Dockerfile.aws.lightsail

docker container run --rm \
    -v `pwd`/app:/app \
    -p 8080:8000 \
    image-generator:lightsail --reload
```

</details>

<details><summary>setup SageMaker</summary>

```bash
docker build -t image-generator:sagemaker . -f ./Dockerfile.aws.sagemaker

docker container run --rm \
    -v `pwd`/app:/app \
    -p 8080:8080 \
    image-generator:sagemaker serve --local --port 8080
```

</details>

```json
{
  "image_url": "https://raw.githubusercontent.com/Fantasy-Studio/Paint-by-Example/main/examples/image/example_1.png",
  "mask_url": "https://raw.githubusercontent.com/Fantasy-Studio/Paint-by-Example/main/examples/mask/example_1.png",
  "example_url": "https://raw.githubusercontent.com/Fantasy-Studio/Paint-by-Example/main/examples/reference/example_1.jpg"
}
```