from prefect import flow, task, get_run_logger
from prefect.deployments import run_deployment
from prefect.filesystems import S3

import asyncio


@task(name="extract task")
def extract() -> None:
    logger = get_run_logger()
    logger.info(f"download from s3")


@task(name="transform task")
def transform() -> None:
    logger = get_run_logger()
    logger.info("transform extract dataset")


@task(name="load task")
def load() -> None:
    logger = get_run_logger()
    logger.info(f"upload to s3")


@flow(name="subflow-name", flow_run_name="{num}", persist_result=True, result_storage=S3(bucket_path="prefect-result-storage"))
def sub_flow(num):
    logger = get_run_logger()
    logger.info("Sub flow start")

    extract()
    transform()
    load()

    if num == 1:
        raise ValueError
    logger.info("Sub flow finished")
    return num


@task(name="train task", log_prints=True)
def train(result):
    print("train task start")

    print(f"arg result:{result}")
    print("train task end")


@task(name="validate task", log_prints=True)
def validate():
    print("validate task start")
    print("validate task end")


@flow(name="mainflow-name", persist_result=True, result_storage=S3(bucket_path="prefect-result-storage"))
async def main_flow():
    logger = get_run_logger()
    logger.info("Main flow start")

    worker_flow_runs = await asyncio.gather(
        *[
            run_deployment(
                name="subflow-name/subflow-deployment",
                parameters=dict(num=num),
            )
            for num in range(5)
        ]
    )
    result = [await run.state.result().get() for run in worker_flow_runs]

    train(result)
    validate()
    logger.info(f"sub flow result: {result}")
    logger.info("Main flow finished")


if __name__ == "__main__":
    asyncio.run(main_flow())
