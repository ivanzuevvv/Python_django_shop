from django.contrib import admin

from .models import Product, PropertyProduct, ImageProduct, TitleProperty


class PropertyInline(admin.TabularInline):
    model = PropertyProduct
    verbose_name = 'Характеристики'
    verbose_name_plural = "Характеристики"


class GalleryInline(admin.TabularInline):
    model = ImageProduct
    verbose_name = "Отображение"
    verbose_name_plural = "Отображения"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'type_device', 'fabricator', 'model',
        'price', 'stock', "created", "updated", 'available', 'limited',
    ]
    list_editable = ['price', 'stock', 'available', 'limited']
    prepopulated_fields = {'slug': ('type_device', 'fabricator', 'model')}
    inlines = [GalleryInline, PropertyInline]
    fieldsets = (
        (None, {
            'fields': (('type_device', 'fabricator', 'model'), 'slug', )
        }),
        ('Характеристики и описание', {
            'classes': ('extrapretty', 'wide'),
            'fields': ('description', ),
            # 'fields': ('description', 'properties'),
            # 'fields': ('description', 'category', 'properties'),
        }),
        ('Настройки продаж', {
            'classes': ('collapse', 'wide'),
            'fields': (('price', 'stock'), ('available', 'limited'), ),
        }),
    )
    # filter_horizontal = ['properties']


admin.site.register(TitleProperty)
