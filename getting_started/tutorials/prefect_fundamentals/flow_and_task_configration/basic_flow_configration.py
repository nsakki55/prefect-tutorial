import os
from prefect import flow

@flow(name="My Example Flow",
      description="An example flow for a tutorial.",
      version=os.getenv("GIT_COMMIT_SHA"))
def my_flow():
    pass
    # run tasks and subflows

my_flow()