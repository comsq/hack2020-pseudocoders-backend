import time

from celery import shared_task


@shared_task
def create_task(task_type: int):
    time.sleep(task_type * 10)
    return True
