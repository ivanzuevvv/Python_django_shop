from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpRequest
from django.shortcuts import render
from django.views import generic
from django.views.generic import TemplateView, DetailView

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


class ProductDetalView(DetailView):
    model = Product
    template_name = 'app_catalog/product.html'
    context_object_name = 'product'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['review_form'] = ReviewForm()
    #     context['form'] = CartAddProductForm(initial={'quantity': 1})
    #     context['reviews'] = Review.objects.prefetch_related('user').filter(product=self.get_object()).order_by(
    #         '-created')
    #     return context
    #
    # def get_object(self, queryset=None):
    #     time_cache = SiteSettings.load().time_cache_product
    #     if not time_cache:
    #         time_cache = 1
    #     return cache.get_or_set(f'product:{self.kwargs.get("pk")}',
    #                             Product.objects.get(id=self.kwargs.get("pk")), 60 * 60 * time_cache)
    #
    # def post(self, request, pk, slug):
    #     form = ReviewForm(request.POST)
    #     if not request.user.is_authenticated:
    #         raise PermissionDenied()
    #     if form.is_valid:
    #         review = form.save(commit=False)
    #         review.user = request.user
    #         review.product = self.get_object()
    #         review.save()
    #         messages.success(request, 'Отзыв добавлен')
    #     return HttpResponseRedirect(reverse('product_detail', kwargs={"pk": pk, "slug": slug}))