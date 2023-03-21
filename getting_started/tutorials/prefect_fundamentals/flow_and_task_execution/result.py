import time
from prefect import task, flow

@task
def my_task():
    return 1

@flow
def my_flow():
    result = my_task.submit()

if __name__ == "__main__":
    my_flow()