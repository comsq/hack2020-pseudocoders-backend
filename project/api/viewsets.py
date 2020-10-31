from django.http import Http404
from rest_framework.viewsets import ModelViewSet

from .models import Group, Language, Task, TaskCheck, User
from .serialzers import GroupSerializer, LanguageSerializer, TaskSerializer, TaskCheckSerializer, UserSerializer


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


class TaskCheckViewSet(ModelViewSet):
    queryset = TaskCheck.objects.order_by('-date')
    serializer_class = TaskCheckSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
