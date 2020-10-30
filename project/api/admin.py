from django.contrib import admin

from .models import Group, Language, Layout, Task, TaskCheck, User


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'owner')


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')


@admin.register(Layout)
class LayoutAdmin(admin.ModelAdmin):
    pass


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')


@admin.register(TaskCheck)
class TaskCheckAdmin(admin.ModelAdmin):
    list_display = ('date', 'student', 'task', 'language', 'status', 'passed_tests_count', 'tests_count')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('login', 'full_name', 'user_type')
    search_fields = ('first_name', 'last_name', 'login', 'middle_name')
    list_filter = ('user_type',)
