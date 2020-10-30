from django.db import models


# FIXME: на случай доработок после хакатона. По хорошему хэшировать пароли, можно связать с пользователями Django
# а также прикрутить использование токена, а не просто токен гонять
class User(models.Model):
    class TypeChoices(models.TextChoices):
        TEACHER = ('teacher', 'Учитель')
        STUDENT = ('student', 'Студент')

    email = models.EmailField(verbose_name='E-mail', max_length=127)
    login = models.CharField(verbose_name='Логин', max_length=127)
    password = models.CharField(verbose_name='Пароль', max_length=127)

    middle_name = models.CharField(verbose_name='Отчество', max_length=127)
    first_name = models.CharField(verbose_name='Имя', max_length=127)
    last_name = models.CharField(verbose_name='Фамилия', max_length=127)

    birthday = models.DateField(verbose_name='Дата рождения')
    user_type = models.CharField(verbose_name='Роль', choices=TypeChoices.choices, max_length=31)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.login

    def full_name(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'
