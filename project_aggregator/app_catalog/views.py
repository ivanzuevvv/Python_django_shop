from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.views.generic import TemplateView, DetailView

from app_comments.forms import CommentForm
from app_comments.models import CommentProduct
from app_configurations.models import SiteSettings
from app_movement_goods.forms import CartAddProductForm
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


class ProductDetalView(DetailView):
    model = Product
    template_name = 'app_catalog/product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = CommentForm()
        context['form'] = CartAddProductForm(initial={'quantity': 1})
        context['reviews'] = (
            CommentProduct.objects.select_related('author', 'product').
            filter(product=self.get_object()).order_by('-pub_at'))
        return context

    def get_object(self, queryset=None):
        time_cache = SiteSettings.load().time_cache_data
        if not time_cache:
            time_cache = 1
        return cache.get_or_set(f'product:{self.kwargs.get("slug")}',
                                Product.objects.get(slug=self.kwargs.get("slug")), 60 * 60 * time_cache)

    def post(self, request, slug):
        form = CommentForm(request.POST)
        if not request.user.is_authenticated:
            raise PermissionDenied()
        if form.is_valid:
            comment = form.save(commit=False)
            comment.author = request.user
            comment.product = self.get_object()
            comment.save()
            messages.success(request, 'Отзыв добавлен')
        return HttpResponseRedirect(reverse('product_detail', kwargs={"slug": slug}))
