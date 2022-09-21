from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Address, UserProfile
from django.utils.html import format_html

class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name',  'is_active']

    list_display_links = ['email']
    readonly_fields = ['last_login', 'date_joined']
    ordering = ['-date_joined']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius:50% ;">' .format(object.profile_picture.url))
    thumbnail.short_description = 'Profile picture'
    list_display = ('thumbnail', 'user', 'date_of_birth', 'location')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Address)
admin.site.register(UserProfile, UserProfileAdmin)