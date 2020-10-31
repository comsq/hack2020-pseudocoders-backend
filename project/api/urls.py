from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    login,
    create_task,
    user_tasks,
    user_task_checks,
    update_task,
)
from .viewsets import GroupViewSet, LanguageViewSet, TaskViewSet, TaskCheckViewSet, UserViewSet


router = DefaultRouter()
router.register(r'groups', GroupViewSet, basename='groups'),
router.register(r'languages', LanguageViewSet, basename='languages'),
router.register(r'tasks', TaskViewSet, basename='tasks'),
router.register(r'task_checks', TaskCheckViewSet, basename='task_checks'),
router.register(r'users', UserViewSet, basename='user')


app_name = 'api'
urlpatterns = [
    path('login/', login, name='login'),
    path('tasks/create/', create_task, name='create_task'),
    path('tasks/update/<int:task_id>/', update_task, name='update_task'),
    path('users/<int:user_id>/tasks/', user_tasks, name='user_tasks'),
    path('users/<int:user_id>/task_checks/', user_task_checks, name='user_task_checks'),
] + router.urls
