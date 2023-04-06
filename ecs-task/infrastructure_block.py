from prefect.infrastructure import DockerContainer

block = DockerContainer(env={
  "EXTRA_PIP_PACKAGES": "s3fs pandas prefect-aws"
})

block.save("etl-docker-container-block")