from django.contrib import admin
from django.utils.timezone import now, localtime

from app_comments.models import ProxyProduct, CommentProduct


@admin.register(CommentProduct)
class CommentAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if obj.hide_on:
            obj.content = f'{obj.content}\n\n Скрыто модератором {request.user.email} {localtime().strftime("%d-%m-%Y %H:%M")}'
        super().save_model(request, obj, form, change)


@admin.register(ProxyProduct)
class ProxyProductAdmin(admin.ModelAdmin):
    date_hierarchy = 'comments__pub_at'
    list_display = [
        '__str__', 'get_count_comments',
        'get_last_comments_pub_at',
        'get_last_comments_author',
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(comments__isnull=False)
