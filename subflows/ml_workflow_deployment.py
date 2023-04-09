from ml_workflow_flow import ml_workflow
from prefect.deployments import Deployment
from prefect_aws.ecs import ECSTask
from prefect.filesystems import S3

storage = S3.load("etl-s3-block")
ecs_task_block = ECSTask.load("ecs-task-block")

deployment = Deployment.build_from_flow(
    flow=ml_workflow,
    name="ml-workflow-deployment",
    version=1,
    storage=storage,
    parameters={
        "model_setting": {
            model_name: ({"is_train": False, "cpu": cpu, "memory": memory})
            for model_name, cpu, memory in zip(
                ["model1", "model2", "model3", "model4", "model5"],
                [1024, 512, 2048, 4096, 1024],
                [2048, 1024, 4096, 8182, 2048],
            )
        },
        "revision": "2023-04-08 12:00:00",
    },
    # work_queue_name="dev-ecs",
    infrastructure=ecs_task_block,
    tags=["dev"],
)

deployment.apply()
