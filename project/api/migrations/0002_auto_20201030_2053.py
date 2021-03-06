# Generated by Django 3.1.2 on 2020-10-30 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63, verbose_name='Название')),
                ('slug', models.CharField(max_length=31, verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'Язык программирования',
                'verbose_name_plural': 'Языки программирования',
            },
        ),
        migrations.CreateModel(
            name='Layout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=511, verbose_name='Путь до папки')),
                ('slug', models.CharField(max_length=63, verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'Шаблон',
                'verbose_name_plural': 'Шаблоны',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('slug', models.CharField(max_length=63, verbose_name='Слаг')),
                ('tests', models.CharField(max_length=511, verbose_name='Путь до тестов')),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='user_directory_path',
            field=models.CharField(default='/tmp/', max_length=511, verbose_name='Папка пользователя'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='login',
            field=models.CharField(max_length=127, unique=True, verbose_name='Логин'),
        ),
        migrations.CreateModel(
            name='TaskCheck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('running', 'В процессе'), ('stopped', 'Остановлена'), ('ce', 'Compilation Error'), ('re', 'Runtime Error'), ('tle', 'Time Limit Exceeded'), ('wa', 'Wrong Answer'), ('ok', 'OK')], default='running', max_length=31, verbose_name='Статус')),
                ('tests_count', models.IntegerField(verbose_name='Количество тестов')),
                ('passed_tests_count', models.IntegerField(verbose_name='Количество пройденных тестов')),
                ('date', models.DateTimeField(verbose_name='Время сдачи')),
                ('language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.language')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user', verbose_name='Студент')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.task', verbose_name='Задача')),
            ],
            options={
                'verbose_name': 'Результат проверки',
                'verbose_name_plural': 'Результаты проверки',
            },
        ),
        migrations.AddField(
            model_name='task',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user', verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='task',
            name='languages',
            field=models.ManyToManyField(to='api.Language', verbose_name='Языки'),
        ),
        migrations.AddField(
            model_name='task',
            name='layout',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.layout', verbose_name='Шаблон'),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127, verbose_name='Группа')),
                ('slug', models.CharField(max_length=63, verbose_name='Слаг')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user')),
                ('tasks', models.ManyToManyField(to='api.Task')),
            ],
            options={
                'verbose_name': 'Группа',
                'verbose_name_plural': 'Группы',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(to='api.Group', verbose_name='Группы'),
        ),
        migrations.AddField(
            model_name='user',
            name='tasks',
            field=models.ManyToManyField(to='api.Task'),
        ),
    ]
