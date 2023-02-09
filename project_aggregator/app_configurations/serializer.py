from rest_framework import serializers

from .models import SiteSettings


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = ['cost_usual_delivery', 'cost_express_delivery', 'min_cost_for_free_delivery', 'root_category',
                  'category_main_page', 'quantity_top_product', 'time_cache_data']
