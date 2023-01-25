from django.contrib import admin

from .models import UserCart, InsideCart


class InsideCartInline(admin.TabularInline):
    model = InsideCart
    verbose_name = 'Товар'
    verbose_name_plural = "Товары в корзине"


@admin.register(UserCart)
class UserCartAdmin(admin.ModelAdmin):
    inlines = [InsideCartInline]
