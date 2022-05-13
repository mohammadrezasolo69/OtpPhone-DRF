from django.contrib import admin
from django.contrib.auth import get_user_model

USER = get_user_model()


@admin.register(USER)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone', 'first_name', 'is_staff', 'is_superuser']
