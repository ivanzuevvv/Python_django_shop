from django.contrib import admin
from django.contrib.auth.models import Group

from app_users.models import User, ProxyGroups


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'email', 'phone', 'get_image_avatar', 'avatar', 'id']
    # add_fieldsets = (
    #     (
    #         None,
    #         {
    #             "classes": ("wide",),
    #             "fields": ("email", "password1", "password2"),
    #         },
    #     ),
    # )


admin.site.unregister(Group)
admin.site.register(ProxyGroups)
