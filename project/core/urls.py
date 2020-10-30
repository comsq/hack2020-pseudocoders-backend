from django.contrib import admin
from django.urls import include, path

from tasks.views import home

urlpatterns = (
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('tasks/', include('tasks.urls')),
    path('', home, name='home'),
)
