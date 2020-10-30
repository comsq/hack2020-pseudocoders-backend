from json import loads

from django.http import JsonResponse, HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import ListAPIView

from .models import Group, Language, Task, TaskCheck, User
from .serialzers import GroupSerializer, LanguageSerializer, TaskSerializer, TaskCheckSerializer, UserSerializer


@csrf_exempt
def login(req: HttpRequest):
    if req.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    req_data = loads(req.body)
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


class GroupListView(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class LanguageListView(ListAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class TaskListView(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskCheckListView(ListAPIView):
    queryset = TaskCheck.objects.all()
    serializer_class = TaskCheckSerializer


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
