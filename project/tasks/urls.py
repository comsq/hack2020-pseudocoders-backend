from django.urls import path

from .views import (
    get_status,
    run_task,
    start_editor,
    stop_editor,
    editor_status,
    verify_task,
)

app_name = 'tasks'
urlpatterns = [
    path('editor/<int:user_id>/start/', start_editor, name='start_editor'),
    path('editor/<int:user_id>/stop/', stop_editor, name='stop_editor'),
    path('editor/<int:user_id>/status/', editor_status, name='editor_status'),
    path('verify/user/<int:user_id>/task/<int:task_id>/language/<int:language_id>', verify_task, name='verify_task'),
    path('<task_id>/', get_status, name='get_status'),
    path('', run_task, name='run_task'),
]
