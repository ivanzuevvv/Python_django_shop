from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpRequest
from django.shortcuts import render
from django.views import generic
from django.views.generic import TemplateView

from app_configurations.models import SiteSettings
from .models import Product


def index(request: HttpRequest):
    return render(request, 'base.html')


class ShopView(TemplateView):
    template_name = 'app_catalog/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        quantity = SiteSettings.load()
        context['products'] = (
            Product.objects.select_related('category').filter(available=True).
            only('category', 'type_device', 'fabricator', 'model', 'price')[:quantity.quantity_top_product]
            # Product.objects.prefetch_related('order_items').select_related('category').
            # filter(available=True).only('category', 'get_full_name', 'price').
            # annotate(total=Sum('order_items__quantity')).order_by('-total')[:quantity.quantity_top_product]
        )
        context['limited'] = (
            Product.objects.select_related('category').
            filter(available=True, limited=True).only('category', 'type_device', 'fabricator', 'model', 'price')
        )
        return context


class AccountView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'app_catalog/account.html'
    raise_exception = True
