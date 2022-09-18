from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Address

class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name',  'is_active']

    list_display_links = ['email']
    readonly_fields = ['last_login', 'date_joined']
    ordering = ['-date_joined']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Address)