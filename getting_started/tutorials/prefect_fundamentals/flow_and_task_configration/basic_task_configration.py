from prefect import flow, task

@task(name="My Example Task",
      description="An example task for a tutorial.",
      tags=["tutorial","tag-test"],
      task_run_name = "hello-{name}-on-{date:%A}")
def my_task():
    pass
    # do some work

@flow
def my_flow():
    my_task()