import json
import os

from django.conf import settings
from django.http import JsonResponse, HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import ModelViewSet

from .models import Group, Language, Task, TaskCheck, User
from .serialzers import GroupSerializer, LanguageSerializer, TaskSerializer, TaskCheckSerializer, UserSerializer
from .tools import generate_slug


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
            with open(settings.TESTS_DIR / slug / f'intput_{i}.txt', 'w') as f:
                f.write(test['input'])
            with open(settings.TESTS_DIR / slug / f'output_{i}.txt', 'w') as f:
                f.write(test['output'])

        task = Task.objects.create(
            name=req_data['name'],
            description=req_data['description'],
            slug=slug,
            author=author,
        )

        task.languages.set(languages)

        return HttpResponse(status=201)

    return HttpResponseNotAllowed(['POST'])


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class LanguageViewSet(ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskCheckViewSet(ModelViewSet):
    queryset = TaskCheck.objects.order_by('-date')
    serializer_class = TaskCheckSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
