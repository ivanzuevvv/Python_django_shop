from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render
from django.views import generic
from django.views.generic import TemplateView

from .models import Product


def index(request: HttpRequest):
    return render(request, 'base.html')


class ShopView(TemplateView):
    template_name = 'app_catalog/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # quantity = SiteSettings.load()
        context['products'] = Product.objects. \
                                  prefetch_related('order_items'). \
                                  filter(available=True). \
                                  only('category', 'name', 'price'). \
                                  annotate(total=Sum('order_items__quantity')). \
                                  order_by('-total')[:quantity.quantity_popular]
        context['limited'] = Product.objects. \
            select_related('category'). \
            filter(available=True). \
            filter(limited=True). \
            only('category', 'name', 'price')
        return context


class AccountView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'app_catalog/account.html'
    raise_exception = True
