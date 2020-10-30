from django.urls import path

from .views import login, GroupListView, LanguageListView, TaskCheckListView, TaskListView, UserListView


app_name = 'api'
urlpatterns = [
    path('groups/', GroupListView.as_view(), name='groups'),
    path('languages/', LanguageListView.as_view(), name='languages'),
    path('tasks/', TaskListView.as_view(), name='tasks'),
    path('task_checks/', TaskCheckListView.as_view(), name='task_checks'),
    path('users/', UserListView.as_view(), name='users'),
    path('login/', login, name='login'),
]
