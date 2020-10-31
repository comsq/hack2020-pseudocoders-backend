from secrets import choice
from string import ascii_lowercase
from typing import Any, Dict, Optional

from .models import Task, TaskCheck, User


def get_verdict(user: User, task: Task) -> Optional[str]:
    all_checks = TaskCheck.objects.filter(user=user, task=task).order_by('-date')
    if len(all_checks) == 0:
        return None
    for task_check in all_checks:  # type: TaskCheck
        if task_check.status == TaskCheck.StatusChoices.OK:
            return task_check.status
    return all_checks[0].status


def generate_slug(length: int = 30) -> str:
    letters = [None for _ in range(length)]
    for i in range(length):
        letters[i] = choice(ascii_lowercase)
    return ''.join(letters)


def serialize_task(task: Task, verdict: Optional[str] = None) -> Dict[str, Any]:
    serialize_task = {
        "id": task.id,
        "author": {
            "id": task.author.id,
            "login": task.author.login,
            "last_name": task.author.last_name,
            "first_name": task.author.first_name,
        },
        "languages": list(map(lambda l: {'id': l.id, 'slug': l.slug, 'name': l.name}, task.languages.all())),
        "name": task.name,
        "description": task.description,
        "slug": task.slug,
        "layout": task.layout_id,
    }

    if verdict:
        serialize_task.update({'verdict': verdict})

    return serialize_task


def serialize_task_check(task_check: TaskCheck) -> Dict[str, Any]:
    return {
        "id": task_check.id,
        "user": {
            "id": task_check.user.id,
            "login": task_check.user.login,
            "last_name": task_check.user.last_name,
            "first_name": task_check.user.first_name,
        },
        "task_author": {
            "id": task_check.task.author.id,
            "login": task_check.task.author.login,
            "last_name": task_check.task.author.last_name,
            "first_name": task_check.task.author.first_name,
        },
        "task": {
            "id": task_check.task.id,
            "name": task_check.task.name,
            "slug": task_check.task.slug,
        },
        "language": {
            "id": task_check.language.id,
            "name": task_check.language.name,
            "slug": task_check.language.slug,
        },
        "date": int(task_check.date.timestamp() * 1000),
        "status": task_check.status,
        "tests_count": task_check.tests_count,
        "passed_tests_count": task_check.passed_tests_count,
    }
