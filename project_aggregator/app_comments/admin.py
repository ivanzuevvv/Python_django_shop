from django import forms
from django.contrib import admin
from django.utils.timezone import now, localtime

from app_comments.models import ProxyProduct, CommentProduct


@admin.register(CommentProduct)
class CommentAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}

    def save_model(self, request, obj, form, change):
        if obj.hide_on:
            obj.content = (f'{obj.content}\n\n'
                           f'Скрыто модератором {request.user.email} {localtime().strftime("%d-%m-%Y %H:%M")}')
        super().save_model(request, obj, form, change)


class CommentProductInline(admin.StackedInline):
    model = CommentProduct
    verbose_name = "Отзыв"
    verbose_name_plural = "Отзывы"
    extra = 0
    add_fieldsets = (None, {'fields': ("author", 'product', "content", "hide_on")})


@admin.register(ProxyProduct)
class ProxyProductAdmin(admin.ModelAdmin):
    ordering = 'comments__pub_at',
    date_hierarchy = 'comments__pub_at'
    list_display = [
        '__str__', 'get_count_comments',
        'get_last_comments_pub_at',
        'get_last_comments_author']
    inlines = [CommentProductInline]
    readonly_fields = ('get_full_name',)
    fields = ['get_full_name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(comments__isnull=False)
