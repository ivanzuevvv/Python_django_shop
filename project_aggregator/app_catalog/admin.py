from django.contrib import admin

from .models import Product, PropertyProduct, ImageProduct, TitleProperty, ExtraData, TitleData, ValueData


def register_hidden_models(*model_names):
    for model in model_names:
        model_admin = type(
            str(model)+'Admin',
            (admin.ModelAdmin,),
            {
                'get_model_perms': lambda self, request: {}
            })
        admin.site.register(model, model_admin)


class PropertyInline(admin.TabularInline):
    model = PropertyProduct
    verbose_name = 'Характеристики'
    verbose_name_plural = "Характеристики"
    extra = 0


class ExstraDataInline(admin.TabularInline):
    model = ExtraData
    verbose_name = 'Дополнительные данные'
    verbose_name_plural = "Сведения"
    extra = 0


class GalleryInline(admin.TabularInline):
    model = ImageProduct
    verbose_name = "Отображение"
    verbose_name_plural = "Отображения"
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    ordering = ["available", 'id']
    list_filter = ["category", 'available', 'limited']
    list_display = [
        'id', 'get_full_name', 'price', 'stock',
        "created", "updated", 'available', 'limited',
    ]
    list_display_links = ['get_full_name']
    list_editable = ['price', 'stock', 'available', 'limited']
    prepopulated_fields = {'slug': ('type_device', 'fabricator', 'model')}
    inlines = [
        ExstraDataInline,
        PropertyInline,
        GalleryInline,
    ]
    fieldsets = (
        (None, {
            'fields': (('type_device', 'fabricator', 'model'), 'slug',)
        }),
        ('Настройки продаж', {
            'classes': 'wide',
            # 'classes': ('collapse', 'wide'),
            'fields': (('price', 'stock'), ('available', 'limited'),),
        }),
        ('Категория и описание', {
            'classes': 'wide',
            'fields': ('category', 'description',),
        }),)


# admin.site.register(TitleProperty)
# admin.site.register(TitleData)
register_hidden_models(TitleProperty, TitleData, ValueData)
