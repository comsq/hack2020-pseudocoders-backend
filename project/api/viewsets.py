from django.db.models import Q
from django.http import HttpRequest, Http404
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .models import Group, Language, Task, TaskCheck, User
from .serialzers import (
    GroupSerializer,
    LanguageSerializer,
    TaskSerializer,
    TaskCheckSerializer,
    TaskWithExamplesSerializer,
    UserSerializer,
)


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class LanguageViewSet(ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'slug'

    def retrieve(self, request: HttpRequest, slug=None):
        task = Task.objects.filter(Q(id=slug) | Q(slug=slug)).first()
        if task is None:
            raise Http404('no task')
        return Response(TaskWithExamplesSerializer(task).data)


class TaskCheckViewSet(ModelViewSet):
    queryset = TaskCheck.objects.order_by('-date')
    serializer_class = TaskCheckSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
