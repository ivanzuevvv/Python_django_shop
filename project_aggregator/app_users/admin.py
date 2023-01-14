from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Group

from app_users.models import User, ProxyGroups
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(Group)
admin.site.register(ProxyGroups)


@admin.register(User)
class MyUserAdmin(UserAdmin):
    ordering = ("id",)
    fieldsets = (
        (None, {"fields": ("email", 'phone', "password")}),
        ("Личная информация", {"fields": ("full_name", "avatar")}),
        ("Права", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Важные даты", {"fields": ("last_login", 'date_joined')}))

    add_fieldsets = (
        (None, {'fields': ("email", 'phone', "password1", "password2")}),)

    filter_horizontal = ("groups", "user_permissions")

    list_display = ['id', 'full_name', 'email', 'phone', 'get_image_avatar',
                    'avatar', "is_active", "is_staff", ]

    list_editable = ["is_active", ]
