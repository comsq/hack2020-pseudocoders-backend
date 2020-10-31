from typing import Tuple

from celery import shared_task
from django.conf import settings
from docker import from_env as docker_client

from api import models


COMPILATION_ERROR_CODE = 11
TIME_LIMIT_ERROR_CODE = 12
RUNTIME_ERROR_CODE = 13
WRONG_ANSWER_ERROR_CODE = 20


def get_verdict(status_code: int) -> Tuple[models.TaskCheck.StatusChoices, int]:
    if status_code == 0:
        return models.TaskCheck.StatusChoices.OK, -1

    if status_code == COMPILATION_ERROR_CODE:
        return models.TaskCheck.StatusChoices.CE, 0

    if status_code == TIME_LIMIT_ERROR_CODE:
        return models.TaskCheck.StatusChoices.TLE, 0

    if status_code == RUNTIME_ERROR_CODE:
        return models.TaskCheck.StatusChoices.RE, 0

    if status_code >= WRONG_ANSWER_ERROR_CODE:
        return models.TaskCheck.StatusChoices.WA, status_code - WRONG_ANSWER_ERROR_CODE

    return models.TaskCheck.StatusChoices.RE, 0


@shared_task
def verify(user_id: int, task_id: int, language_id: int):
    user = models.User.objects.get(id=user_id)
    task = models.Task.objects.get(id=task_id)
    language = models.Language.objects.get(id=language_id)

    user_solution = user.directory / 'project' / task.slug
    task_tests = task.tests_directory

    task_check = models.TaskCheck.objects.create(
        user=user,
        task=task,
        language=language,
        passed_tests_count=0,
        tests_count=len(list(task_tests.glob('input_*.txt'))),
    )

    docker = docker_client()

    container = docker.containers.run(
        f'dimastark/{language.slug}-runner',
        detach=True,
        volumes={
            str(user_solution.absolute()): dict(bind='/source', mode='rw'),
            str(task_tests.absolute()): dict(bind='/tests', mode='rw'),
        },
    )

    result = container.wait()
    logs = container.logs()
    status_code = result['StatusCode']
    container.remove()

    verdict_status, verdict_passed_tests_count = get_verdict(status_code)

    if verdict_passed_tests_count == -1:
        verdict_passed_tests_count = task_check.tests_count

    task_check.status = verdict_status
    task_check.passed_tests_count = verdict_passed_tests_count
    task_check.save()

    return logs.decode()
