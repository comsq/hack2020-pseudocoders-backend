import os

from django.conf import settings
from rest_framework import serializers
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
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if fields:
            for field_name in list(self.fields):
                if field_name not in fields:
                    self.fields.pop(field_name)

    author = serializers.SerializerMethodField(method_name='get_author')
    languages = serializers.SerializerMethodField(method_name='get_languages')

    class Meta:
        model = Task
        fields = '__all__'

    def get_author(self, obj: Task):
        return UserSerializer(obj.author, fields=('id', 'first_name', 'last_name', 'login')).data

    def get_languages(self, obj: Task):
        return LanguageSerializer(obj.languages.all(), many=True).data


class TaskCheckSerializer(ModelSerializer):
    user = serializers.SerializerMethodField(method_name='get_user')
    task = serializers.SerializerMethodField(method_name='get_task')
    language = serializers.SerializerMethodField(method_name='get_language')
    date = serializers.SerializerMethodField(method_name='get_date_in_ms')

    class Meta:
        model = TaskCheck
        fields = '__all__'

    def get_user(self, obj: TaskCheck):
        return UserSerializer(obj.user, fields=('id', 'first_name', 'last_name', 'login')).data

    def get_task(self, obj: TaskCheck):
        return TaskSerializer(obj.task, fields=('id', 'name', 'slug')).data

    def get_language(self, obj: TaskCheck):
        return LanguageSerializer(obj.language).data

    def get_date_in_ms(self, obj: TaskCheck):
        return int(obj.date.timestamp() * 1000)


class TaskWithExamplesSerializer(TaskSerializer):
    tests = serializers.SerializerMethodField(method_name='get_examples')

    def get_examples(self, obj: Task):
        tests = []
        for i in range(1, 4):
            inp_file = settings.TESTS_DIR / obj.slug / f'input_{i}.txt'
            if not os.path.exists(inp_file):
                break
            out_file = settings.TESTS_DIR / obj.slug / f'output_{i}.txt'
            with open(inp_file) as f:
                inp = f.read()
            with open(out_file) as f:
                out = f.read()
            tests.append({'input': inp, 'output': out})
        return tests


class UserSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if fields:
            for field_name in list(self.fields):
                if field_name not in fields:
                    self.fields.pop(field_name)

    class Meta:
        model = User
        exclude = ('password',)
