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