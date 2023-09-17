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

```shell
python script/predict.py -n image-generator script/test.json
```

</details>