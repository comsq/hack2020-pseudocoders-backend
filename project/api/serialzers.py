from rest_framework.serializers import ModelSerializer

from .models import Group, Language, Task, TaskCheck, User


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class LanguageSerializer(ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TaskCheckSerializer(ModelSerializer):
    class Meta:
        model = TaskCheck
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
