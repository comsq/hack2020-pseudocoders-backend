import json

from celery.result import AsyncResult
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

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
def get_status(request: HttpRequest, task_id: str) -> HttpResponse:
    task_result = AsyncResult(task_id)

    result = {
        'task_id': task_id,
        'task_status': task_result.status,
        'task_result': task_result.result,
    }

    return JsonResponse(result, status=200)