from ml_workflow_flow import train_flow
from prefect.deployments import Deployment
from prefect_aws.ecs import ECSTask
from prefect.filesystems import S3

storage = S3.load("etl-s3-block")
ecs_task_block = ECSTask.load("ecs-task-block")

deployment = Deployment.build_from_flow(
    flow=train_flow,
    name="train-subflow-deployment",
    version=1,
    work_pool_name="local",
    # work_queue_name="dev-ecs",
    infrastructure=ecs_task_block,
    storage=storage,
    tags=["dev"],
)

deployment.apply()
