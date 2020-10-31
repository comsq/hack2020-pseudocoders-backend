import json
import os

from celery.result import AsyncResult
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from api import models
from tasks import code_editor, task_check
from tasks.sample_tasks import create_task


def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'home.html')


@csrf_exempt
def run_task(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    try:
        task_type = int(json.loads(request.body).get('type'))
    except ValueError:
        return HttpResponseBadRequest()

    result = {
        'task_id': create_task.delay(task_type).id,
    }

    return JsonResponse(result, status=202)


@csrf_exempt
def start_editor(request: HttpRequest, user_id: int) -> HttpResponse:
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    try:
        user = models.User.objects.get(id=user_id)
    except models.User.DoesNotExist:
        return HttpResponseBadRequest()

    for task in user.tasks.all():
        os.makedirs(settings.USERS_DIR / user.login / 'project' / task.slug, exist_ok=True)

    for group in user.groups.all():
        for task in group.tasks.all():
            os.makedirs(settings.USERS_DIR / user.login / 'project' / task.slug, exist_ok=True)

    result = {
        'task_id': code_editor.start.delay(user_id).id,
    }

    return JsonResponse(result, status=202)


@csrf_exempt
def stop_editor(request: HttpRequest, user_id: int) -> HttpResponse:
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    try:
        models.User.objects.get(id=user_id)
    except models.User.DoesNotExist:
        return HttpResponseBadRequest()

    result = {
        'task_id': code_editor.stop.delay(user_id).id,
    }

    return JsonResponse(result, status=202)


@csrf_exempt
def editor_status(request: HttpRequest, user_id: int) -> HttpResponse:
    try:
        user = models.User.objects.get(id=user_id)
    except models.User.DoesNotExist:
        return HttpResponseBadRequest()

    result = {
        'status': code_editor.status(user_id),
        'port': user.editor_port,
    }

    return JsonResponse(result, status=202)


@csrf_exempt
def verify_task(request: HttpRequest, user_id: int, task_id: int, language_id: int) -> HttpResponse:
    try:
        models.User.objects.get(id=user_id)
    except models.User.DoesNotExist:
        return HttpResponseBadRequest()

    try:
        models.Task.objects.get(id=task_id)
    except models.Task.DoesNotExist:
        return HttpResponseBadRequest()

    try:
        models.Language.objects.get(id=language_id)
    except models.Language.DoesNotExist:
        return HttpResponseBadRequest()

    result = {
        'task_id': task_check.verify.delay(user_id, task_id, language_id).id,
    }

    return JsonResponse(result, status=202)


@csrf_exempt
def get_status(request: HttpRequest, task_id: str) -> HttpResponse:
    task_result = AsyncResult(task_id)

    result = {
        'task_id': task_id,
        'task_status': task_result.status,
        'task_result': task_result.result,
    }

    return JsonResponse(result, status=200)
