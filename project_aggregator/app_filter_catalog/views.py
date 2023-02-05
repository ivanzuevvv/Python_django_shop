from django.shortcuts import render
from django_filters.views import FilterView

from app_configurations.models import SiteSettings, Category
from .filters import ProductFilter
from .utils import get_data_min, get_data_max
from app_products.models import Product


class ProductByCategoryView(FilterView):
    paginate_by = 8
    model = Product
    settings = None
    category = None
    context_object_name = 'products'
    filterset_class = ProductFilter
    template_name = 'app_filter_catalog/catalog.html'

    def get(self, request, *args, **kwargs):
        self.settings = SiteSettings.load()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        if not slug:
            self.category = self.settings.root_category
        else:
            self.category = Category.objects.get(slug=slug)
        sub_categories = self.category.get_descendants(include_self=True)
        queryset = Product.objects.select_related('category').\
            only('category', 'type_device', 'fabricator', 'model', 'price').filter(
            category__in=sub_categories).filter(available=True)
        return queryset

    def get_context_data(self, **kwargs):
        _request_copy = self.request.GET.copy()
        parameters = _request_copy.pop('page', True) and _request_copy.urlencode()
        context = super().get_context_data(**kwargs)
        context['title'] = self.category
        qs = self.get_queryset()
        min_price = get_data_min(queryset=qs, root_category=self.settings.root_category)
        max_price = get_data_max(queryset=qs, root_category=self.settings.root_category)
        context['parameters'] = parameters
        context['filter'].form.fields['price'].widget.attrs = {'class': 'range-line',
                                                               'data-type': 'double',
                                                               'data-min': min_price,
                                                               'data-max': max_price}
        return context
