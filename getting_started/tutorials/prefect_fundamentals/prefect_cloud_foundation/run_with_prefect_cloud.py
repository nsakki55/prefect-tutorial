from prefect import flow, get_run_logger

@flow(name="Prefect Cloud Quickstart")
def quickstart_flow():
    logger = get_run_logger()
    logger.warning("Local quickstart flow is running!")

if __name__ == "__main__":
    quickstart_flow()