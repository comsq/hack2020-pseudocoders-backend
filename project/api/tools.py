from secrets import choice
from string import ascii_lowercase
from typing import Any, Dict

from .models import Task, TaskCheck


def generate_slug(length: int = 30) -> str:
    letters = [None for _ in range(length)]
    for i in range(length):
        letters[i] = choice(ascii_lowercase)
    return ''.join(letters)


def serialize_task(task: Task) -> Dict[str, Any]:
    return {
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


def serialize_task_check(task_check: TaskCheck) -> Dict[str, Any]:
    return {
        "id": task_check.id,
        "user": {
            "id": task_check.user.id,
            "login": task_check.user.login,
            "last_name": task_check.user.last_name,
            "first_name": task_check.user.first_name,
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
