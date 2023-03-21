from prefect import flow, task
from prefect.task_runners import SequentialTaskRunner

@task
def say_hello(name):
    print(f"hello {name}")

@task
def say_goodbye(name):
    print(f"goodbye {name}")

@flow(task_runner=SequentialTaskRunner())
def greetings(names):
    for name in names:
        say_hello.submit(name)
        say_goodbye.submit(name)

greetings(["arthur", "trillian", "ford", "marvin"])