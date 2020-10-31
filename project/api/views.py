import json
import os
import shutil

from django.db.utils import IntegrityError
from django.conf import settings
from django.http import JsonResponse, HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from .models import Group, Language, Task, TaskCheck, User
from .tools import generate_slug, serialize_task, serialize_task_check, get_verdict


@csrf_exempt
def login(req: HttpRequest):
    if req.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    req_data = json.loads(req.body)
    login = req_data.get('login')
    password = req_data.get('password')

    user = User.objects.filter(login=login, password=password).first()
    if user is None:
        return HttpResponse(status=401)

    return JsonResponse(
        {
            'id': user.id,
            'login': user.login,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'type': user.user_type,
        }
    )


@csrf_exempt
def create_task(req: HttpRequest):
    if req.method == 'POST':
        req_data = json.loads(req.body)

        slug = req_data.get('slug') or generate_slug(10)

        author_id = req_data.get('author', 1)
        author = User.objects.get(pk=author_id)

        lang_slugs = req_data['languages']
        languages = Language.objects.filter(slug__in=lang_slugs)

        os.makedirs(settings.TESTS_DIR / slug, exist_ok=True)
        tests = req_data['tests']
        for i, test in enumerate(tests, start=1):
            with open(settings.TESTS_DIR / slug / f'input_{i}.txt', 'w') as f:
                f.write(test['input'])
            with open(settings.TESTS_DIR / slug / f'output_{i}.txt', 'w') as f:
                f.write(test['output'])
        try:
            task = Task.objects.create(
                name=req_data['name'],
                description=req_data['description'],
                slug=slug,
                author=author,
            )
        except IntegrityError:
            return HttpResponse('task with slug exists', status=400)

        task.languages.set(languages)

        return HttpResponse(status=201)

    return HttpResponseNotAllowed(['POST'])


@csrf_exempt
def update_task(req: HttpRequest, task_slug: str):
    if req.method != 'PUT':
        return HttpResponseNotAllowed(['PUT'])

    task = Task.objects.filter(slug=task_slug).first()
    if task is None:
        return HttpResponse(status=404)

    req_data = json.loads(req.body)

    slug = req_data.get('slug')
    if slug:
        task.slug = slug

    author_id = req_data.get('author', 1)
    author = User.objects.filter(id=author_id).first()
    if author:
        task.author = author

    if req_data.get('name'):
        task.name = req_data['name']
    if req_data.get('description'):
        task.description = req_data['description']

    languages = None
    if req_data.get('languages'):
        languages = Language.objects.filter(slug__in=req_data['languages'])

    if req_data.get('tests'):
        if os.path.exists(settings.TESTS_DIR / task.slug):
            shutil.rmtree(settings.TESTS_DIR / task.slug)
        os.makedirs(settings.TESTS_DIR / task.slug, exist_ok=True)
        tests = req_data['tests']
        for i, test in enumerate(tests, start=1):
            with open(settings.TESTS_DIR / task.slug / f'input_{i}.txt', 'w') as f:
                f.write(test['input'])
            with open(settings.TESTS_DIR / task.slug / f'output_{i}.txt', 'w') as f:
                f.write(test['output'])

    task.save()

    if languages:
        task.languages.set(languages)

    return HttpResponse(status=200)


@csrf_exempt
def user_tasks(req: HttpRequest, user_id: int):
    """
    FIXME: придумай куда вставить нормально создание директорий с заданиями, создавать пачку директорий на каждый GET
    плохо, но для хакатона пойдёт
    """
    user = User.objects.get(pk=user_id)
    if user is None:
        return HttpResponse(status=404)

    if user.user_type == 'student':
        already_added = set()
        student_tasks = []
        for task in user.tasks.all():  # type: Task
            if task.id in already_added:
                continue
            os.makedirs(settings.USERS_DIR / user.login / 'project' / task.slug, exist_ok=True)
            already_added.add(task.id)
            verdict = get_verdict(user, task)
            student_tasks.append(serialize_task(task, verdict=verdict))

        groups = user.groups.all()
        for group in groups:  # type: Group
            for task in group.tasks.all():
                if task.id in already_added:
                    continue
                os.makedirs(settings.USERS_DIR / user.login / 'project' / task.slug, exist_ok=True)
                already_added.add(task.id)
                verdict = get_verdict(user, task)
                student_tasks.append(serialize_task(task, verdict=verdict))

        return JsonResponse(student_tasks, safe=False)

    elif user.user_type == 'teacher':
        teacher_tasks = [serialize_task(task) for task in Task.objects.filter(author=user)]
        return JsonResponse(teacher_tasks, safe=False)


@csrf_exempt
def user_task_checks(req: HttpRequest, user_id: int):
    user = User.objects.get(pk=user_id)
    if user is None:
        return HttpResponse(status=404)

    if user.user_type == 'student':
        task_checks = [
            serialize_task_check(task_check)
            for task_check in TaskCheck.objects.filter(user_id=user_id).order_by('-date')
        ]
        return JsonResponse(task_checks, safe=False)

    elif user.user_type == 'teacher':
        tasks = Task.objects.filter(author=user)
        return JsonResponse(
            [
                serialize_task_check(task_check)
                for task_check in TaskCheck.objects.filter(task__in=tasks).order_by('-date')
            ],
            safe=False,
        )
