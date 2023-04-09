from prefect import flow, task, get_run_logger, unmapped
from prefect.deployments import run_deployment
from prefect.filesystems import S3
import time
import asyncio


@task(name="extract task")
def extract() -> None:
    logger = get_run_logger()
    logger.info(f"extract task execution")
    time.sleep(10)


@task(name="transform task")
def transform() -> None:
    logger = get_run_logger()
    logger.info("transform task execution")
    time.sleep(10)


@task(name="train task")
def train() -> None:
    logger = get_run_logger()
    logger.info(f"train task execution")

    time.sleep(10)


@task(name="validate task")
def validate() -> None:
    logger = get_run_logger()
    logger.info(f"validate task execution")
    time.sleep(10)


@flow(
    name="train-subflow",
    flow_run_name="{model_name}:{revision}",
    persist_result=True,
    result_storage=S3(bucket_path="prefect-result-storage/result"),
)
def train_flow(model_name, revision):
    logger = get_run_logger()
    logger.info(f"train {model_name} {revision} flow start")
    extract()
    transform()
    train()
    validate()

    logger.info(f"train {model_name} {revision} flow finished")
    return True


@task(name="update predict server task")
def update_predict_server_task(train_subflow_result):
    logger = get_run_logger()
    logger.info(f"update predict server {train_subflow_result}")
    time.sleep(10)
    return True


@task(name="validate data distribution task")
def validate_data_distribution_task(train_subflow_result):
    logger = get_run_logger()
    logger.info(f"valdiate data distribution {train_subflow_result}")
    time.sleep(10)
    return True


@task(name="online model performance task")
def online_model_performance_task(train_subflow_result):
    logger = get_run_logger()
    logger.info(f"online model performance {train_subflow_result}")
    time.sleep(10)
    return True


@task(name="train result task")
def train_result_task(train_subflow_runs):
    logger = get_run_logger()
    logger.info(f"train result task {train_subflow_runs}")
    time.sleep(10)

    return train_subflow_runs


#
# @task(name="train flow task")
# def kick_train_flow(model_name, revision):
#     result = run_deployment(
#         name="train-subflow/train-subflow-deployment",
#         parameters=dict(model_name=model_name, revision=revision),
#     )
#     return True


@flow(
    name="MLWorkFlow",
    flow_run_name="{revision}",
    persist_result=True,
    result_storage=S3(bucket_path="prefect-result-storage/result"),
)
async def ml_workflow(model_setting, revision):
    logger = get_run_logger()
    logger.info("ml workflow start")
    model_names = [model_name for model_name in model_setting.keys()]
    train_subflow_runs = await asyncio.gather(
        *[
            run_deployment(
                name="train-subflow/train-subflow-deployment",
                parameters=dict(model_name=model_name, revision=revision),
            )
            for model_name in model_names
        ]
    )
    # train_subflow_result = kick_train_flow.map(model_names, unmapped(revision))
    train_subflow_result = train_result_task([await run.state.result().get() for run in train_subflow_runs])
    # train_subflow_result = [await run.state.result().get() for run in train_subflow_runs]

    update_predict_server_result = update_predict_server_task(train_subflow_result)
    validate_data_distribution_result = validate_data_distribution_task(update_predict_server_result)
    online_model_performance_task(validate_data_distribution_result)

    logger.info("ml workflow finished")


if __name__ == "__main__":
    # model_setting = {
    #     model_name: ({"is_train": False, "cpu": cpu, "memory": memory})
    #     for model_name, cpu, memory in zip(
    #         ["model1", "model2", "model3", "model4", "model5"], [1024, 512, 2048, 4096, 1024], [2048, 1024, 4096, 8182, 2048]
    #     )
    # }
    model_setting = {
        model_name: ({"is_train": False, "cpu": cpu, "memory": memory})
        for model_name, cpu, memory in zip(["model1", "model2", "model3"], [1024, 512, 2048], [2048, 1024, 4096])
    }
    print(model_setting)
    revision = "2023-04-08 12:00:00"
    asyncio.run(ml_workflow(model_setting, revision))
