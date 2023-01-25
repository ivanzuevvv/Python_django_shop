from django.contrib import admin

from .models import UserCart, InsideCart


class InsideCartInline(admin.TabularInline):
    model = InsideCart
    verbose_name = 'Товар'
    verbose_name_plural = "Товары в корзине"
    fields = ('goods', 'quantity', 'cost')
    readonly_fields = 'cost',
    extra = 0


@admin.register(UserCart)
class UserCartAdmin(admin.ModelAdmin):
    readonly_fields = 'session',
    inlines = [InsideCartInline]
