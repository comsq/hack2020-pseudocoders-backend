# Generated by Django 3.1.2 on 2020-10-31 07:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20201031_0639'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taskcheck',
            old_name='student',
            new_name='user',
        ),
    ]
