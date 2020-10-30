from django.urls import path

from .views import get_status, run_task

app_name = 'tasks'
urlpatterns = [
    path('<task_id>/', get_status, name='get_status'),
    path('', run_task, name='run_task'),
]
