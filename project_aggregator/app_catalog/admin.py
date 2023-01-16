from django.contrib import admin

from .models import Product, PropertyProduct, ImageProduct


# class PropertyInline(admin.TabularInline):
#     model = PropertyProduct


class GalleryInline(admin.TabularInline):
    model = ImageProduct


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'type_device', 'fabricator', 'model',
        'price', 'stock', "created", "updated", 'available', 'limited',
    ]
    list_editable = ['price', 'stock', 'available', 'limited']
    prepopulated_fields = {'slug': ('type_device', 'fabricator', 'model')}
    inlines = [GalleryInline, ]
    fieldsets = (
        (None, {
            'fields': (('type_device', 'fabricator', 'model'), 'slug', )
        }),
        ('Характеристики и описание', {
            'classes': ('extrapretty', 'wide'),
            'fields': ('description', 'properties'),
            # 'fields': ('description', 'category', 'properties'),
        }),
        ('Настройки продаж', {
            'classes': ('collapse', 'wide'),
            'fields': (('price', 'stock'), ('available', 'limited'), ),
        }),
    )
    filter_horizontal = ['properties']
