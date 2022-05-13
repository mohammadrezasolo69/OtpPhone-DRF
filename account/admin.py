from django.contrib import admin
from django.contrib.auth import get_user_model
from account.models import OTP

USER = get_user_model()


@admin.register(USER)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone', 'first_name', 'is_staff', 'is_superuser']

admin.site.register(OTP)