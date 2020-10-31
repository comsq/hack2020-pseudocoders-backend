from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import login, GroupViewSet, LanguageViewSet, TaskCheckViewSet, TaskViewSet, UserViewSet


router = DefaultRouter()
router.register(r'groups', GroupViewSet, basename='groups'),
router.register(r'languages', LanguageViewSet, basename='languages'),
router.register(r'tasks', TaskViewSet, basename='tasks'),
router.register(r'task_checks', TaskCheckViewSet, basename='task_checks'),
router.register(r'users', UserViewSet, basename='user')


app_name = 'api'
urlpatterns = [
    path('login/', login, name='login'),
] + router.urls
