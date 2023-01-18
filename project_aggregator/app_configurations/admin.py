from django.contrib import admin
from django.shortcuts import redirect
from django_mptt_admin.admin import DjangoMpttAdmin

from .models import Category, SiteSettings


class CategoryAdmin(DjangoMpttAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'cost_usual_delivery', 'cost_express_delivery',
        'min_cost_for_free_delivery', 'quantity_top_product',
        'time_cache_data', 'show_category_main_page',
        'root_category',
    ]
    list_editable = [
        'cost_usual_delivery', 'cost_express_delivery',
        'min_cost_for_free_delivery', 'quantity_top_product',
        'time_cache_data', 'root_category',
    ]
    filter_horizontal = ['category_main_page']
    actions = ['edit_configuration']

    @admin.action(description='Редактировать конфигурацию')
    def edit_configuration(self, request, queryset):
        return redirect(f'{queryset[0].id}/change/')


admin.site.register(Category, CategoryAdmin)
