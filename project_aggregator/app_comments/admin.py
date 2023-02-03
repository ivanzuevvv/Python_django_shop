from django.contrib import admin

from app_comments.models import ProxyProduct, CommentProduct


@admin.register(CommentProduct)
class CommentAdmin(admin.ModelAdmin):
    pass


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
