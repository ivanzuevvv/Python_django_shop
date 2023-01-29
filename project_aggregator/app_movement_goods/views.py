from decimal import Decimal

from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import TemplateView

from app_catalog.models import Product
from .forms import CartAddProductForm
from .cart import get_cart


@require_POST
def cart_add(request, pk):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=pk)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        cart.add(
            product=product,
            quantity=data['quantity'],
            update_quantity=data['update'])
    return redirect('cart_detail')


@require_GET
def cart_remove(request, pk):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=pk)
    cart.remove(product)
    return redirect('cart_detail')


class CartDetailView(TemplateView):
    template_name = 'app_cart/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_cart(self.request)
        context['cart'] = cart
        return context


@require_GET
def get_cart_data(request):
    product_id = request.GET.get('product', None)
    cart = get_cart(request)
    response = {
        'total_len': len(cart),
        'total': cart.get_total_price
    }
    if product_id:
        product = cart.contents.get(product_id=product_id)
        total_item = int(product.quantity) * Decimal(product.cost)
        response['total_item'] = total_item
    return JsonResponse(response)


