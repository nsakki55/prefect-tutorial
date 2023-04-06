from etl import etl_flow
from prefect.deployments import Deployment
from prefect.filesystems import S3
from prefect.infrastructure.docker import DockerContainer
from prefect.server.schemas.schedules import CronSchedule

storage = S3.load("etl-s3-block")
infrastructure = DockerContainer.load("etl-docker-container-block")

deployment = Deployment.build_from_flow(
    flow=etl_flow,
    name="etl-flow-deployment",
    version=1,
    work_queue_name="etl",
    storage=storage,
    infrastructure=infrastructure,
    tags=['dev'],
    schedule=(CronSchedule(cron="0 0 * * *", timezone="Asia/Tokyo"))
)

deployment.apply()