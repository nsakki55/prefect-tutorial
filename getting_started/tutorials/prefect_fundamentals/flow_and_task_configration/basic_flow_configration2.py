import datetime
from prefect import flow

@flow(flow_run_name="{name}-on-{date:%A}")
def my_flow(name: str, date: datetime.datetime):
    pass

# creates a flow run called 'marvin-on-Thursday'
my_flow(name="marvin", date=datetime.datetime.utcnow())
