from etl import main_flow
from prefect.deployments import Deployment
from prefect_aws.ecs import ECSTask
from prefect.filesystems import S3

storage = S3.load("etl-s3-block")
ecs_task_block = ECSTask.load("ecs-task-block")

deployment = Deployment.build_from_flow(
    flow=main_flow,
    name="mainflow-deployment",
    version=1,
    storage=storage,
    work_queue_name="dev-ecs",
    infrastructure=ecs_task_block,
    tags=["dev"],
)

deployment.apply()
