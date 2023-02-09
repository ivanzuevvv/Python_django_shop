from django import forms
from django.contrib import admin
from django.db import models
from django.db.models import Count
from django.forms import Textarea
from django.utils.timezone import localtime

from app_comments.models import ProxyProduct, CommentProduct


@admin.register(CommentProduct)
class CommentAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}

    def save_model(self, request, obj, form, change):
        if obj.hide_on:
            obj.content = (f'{obj.content}\n\n'
                           f'Скрыто модератором {request.user.email}\n'
                           f'{localtime().strftime("%d-%m-%Y %H:%M")}')
        super().save_model(request, obj, form, change)


class CommentProductInline(admin.StackedInline):
    model = CommentProduct
    verbose_name = "Отзыв"
    verbose_name_plural = "Отзывы"
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'cols': '100', 'rows': '2'})}}
    show_change_link = True


@admin.register(ProxyProduct)
class ProxyProductAdmin(admin.ModelAdmin):
    ordering = 'id',
    date_hierarchy = 'comments__pub_at'
    list_display = [
        '__str__', 'get_count_comments',
        'get_last_comments_pub_at',
        'get_last_comments_author'
    ]
    inlines = [CommentProductInline]
    readonly_fields = ('get_full_name',)
    fields = ['get_full_name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        myqs = qs.prefetch_related('comments').annotate(num_comm=Count('comments')).exclude(num_comm__lt=1)
        # myqs = qs.prefetch_related('comments').annotate(num_comm=Count('comments')).filter(num_comm__lt=1)
        # myqs1 = qs.prefetch_related('comments').filter(comments__product__id__isnull=False).distinct()
        return myqs
