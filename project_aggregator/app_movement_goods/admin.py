from django.contrib import admin

from .models import UserCart, InsideCart, Order, OrderContents


class InsideCartInline(admin.TabularInline):
    model = InsideCart
    verbose_name = 'Товар'
    verbose_name_plural = "Товары в корзине"
    fields = ('product', 'quantity', 'cost')
    readonly_fields = 'cost',
    extra = 0


@admin.register(UserCart)
class UserCartAdmin(admin.ModelAdmin):
    readonly_fields = 'session',
    inlines = [InsideCartInline]


class OrderContentsInline(admin.TabularInline):
    model = OrderContents
    verbose_name = 'Товар'
    verbose_name_plural = "Товары в заказе"
    fields = ('product', 'quantity', 'price')
    readonly_fields = 'price',
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'get_total_cost', 'created_at', 'updated_at', 'paid']
    list_filter = ['paid', 'created_at', 'delivery_type']
    inlines = [OrderContentsInline]
