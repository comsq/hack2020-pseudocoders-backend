from pathlib import Path

from django.conf import settings
from django.db import models


# FIXME: на случай доработок после хакатона. По хорошему хэшировать пароли, можно связать с пользователями Django
# а также прикрутить использование токена, а не просто id пользователя гонять
class User(models.Model):
    class TypeChoices(models.TextChoices):
        TEACHER = ('teacher', 'Учитель')
        STUDENT = ('student', 'Студент')

    email = models.EmailField(verbose_name='E-mail', max_length=127)
    login = models.CharField(verbose_name='Логин', max_length=127, unique=True)
    password = models.CharField(verbose_name='Пароль', max_length=127)

    last_name = models.CharField(verbose_name='Фамилия', max_length=127)
    first_name = models.CharField(verbose_name='Имя', max_length=127)
    middle_name = models.CharField(verbose_name='Отчество', max_length=127)

    birthday = models.DateField(verbose_name='Дата рождения')
    user_type = models.CharField(verbose_name='Роль', choices=TypeChoices.choices, max_length=31)

    groups = models.ManyToManyField('Group', verbose_name='Группы', blank=True)
    tasks = models.ManyToManyField('Task', verbose_name='Задачи', blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.login

    @property
    def directory(self) -> Path:
        return Path(settings.USERS_DIR) / self.login

    @property
    def editor_name(self) -> str:
        return f'editor-{self.login}'

    @property
    def editor_port(self) -> int:
        return 8000 + self.id

    def get_task_directory(self, task_slug: str) -> Path:
        return self.directory / task_slug

    @property
    def full_name(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'


class Group(models.Model):
    name = models.CharField(verbose_name='Группа', max_length=127)
    slug = models.CharField(verbose_name='Слаг', max_length=63, unique=True)
    tasks = models.ManyToManyField('Task', verbose_name='Задачи', blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.slug


class Task(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    name = models.CharField(verbose_name='Название', max_length=127)
    description = models.TextField(verbose_name='Описание')
    slug = models.CharField(verbose_name='Слаг', max_length=63, unique=True)
    layout = models.ForeignKey('Layout', verbose_name='Шаблон', null=True, on_delete=models.SET_NULL)
    languages = models.ManyToManyField('Language', verbose_name='Языки', blank=True)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    @property
    def tests_directory(self) -> Path:
        return Path(settings.TESTS_DIR) / self.slug

    def __str__(self):
        return self.slug


class Layout(models.Model):
    slug = models.CharField(verbose_name='Слаг', max_length=63, unique=True)

    class Meta:
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны'

    @property
    def directory(self) -> Path:
        return Path(settings.LAYOUTS_DIR) / self.slug

    def __str__(self):
        return self.slug


class TaskCheck(models.Model):
    class StatusChoices(models.TextChoices):
        RUNNING = 'running', 'В процессе'
        STOPPED = 'stopped', 'Остановлена'
        CE = 'ce', 'Compilation Error'
        RE = 're', 'Runtime Error'
        TLE = 'tle', 'Time Limit Exceeded'
        WA = 'wa', 'Wrong Answer'
        OK = 'ok', 'OK'

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Студент')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='Задача')
    status = models.CharField(
        verbose_name='Статус', choices=StatusChoices.choices, max_length=31, default=StatusChoices.RUNNING,
    )
    tests_count = models.IntegerField(verbose_name='Количество тестов')
    passed_tests_count = models.IntegerField(verbose_name='Количество пройденных тестов')
    date = models.DateTimeField(verbose_name='Время сдачи')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Результат проверки'
        verbose_name_plural = 'Результаты проверки'

    def __str__(self):
        return f'{self.user.login} {self.task.slug}'


class Language(models.Model):
    name = models.CharField(verbose_name='Название', max_length=63)
    slug = models.CharField(verbose_name='Слаг', max_length=31, unique=True)

    class Meta:
        verbose_name = 'Язык программирования'
        verbose_name_plural = 'Языки программирования'

    def __str__(self):
        return self.slug
