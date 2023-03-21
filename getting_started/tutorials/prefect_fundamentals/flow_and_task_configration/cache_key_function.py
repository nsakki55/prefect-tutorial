from prefect import flow, task
from datetime import timedelta
import time

def cache_key_from_sum(context, parameters):
    print(parameters)
    return sum(parameters["nums"])

@task(cache_key_fn=cache_key_from_sum, cache_expiration=timedelta(minutes=1))
def cached_task(nums):
    print('running an expensive operation')
    time.sleep(3)
    return sum(nums)

@flow
def test_caching(nums):
    cached_task(nums)

test_caching([1, 2, 3, 4, 5])