from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('login', 'full_name', 'user_type')
    search_fields = ('first_name', 'last_name', 'login', 'middle_name')
    list_filter = ('user_type',)
