from decimal import Decimal

from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import TemplateView

from app_catalog.models import Product
from .forms import CartAddProductForm
from .models import UserCart
from .session_entities import Cart


@require_POST
def cart_add(request, pk):
    if request.user.is_authenticated:
        cart = UserCart.objects.get(owner=request.user)
    else:
        cart = Cart(request)
    product = Product.objects.get(id=pk)
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
    cart = Cart(request)
    product = get_object_or_404(Product, id=pk)
    cart.remove(product)
    return redirect('cart_detail')


class CartDetailView(TemplateView):
    template_name = 'app_cart/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cart = UserCart.objects.get(owner=self.request.user)
        else:
            cart = Cart(self.request)
        context['cart'] = cart
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
            print(f'item={item} cart={cart.cart}')
        return context


@require_GET
def get_cart_data(request):
    product_id = request.GET.get('product', None)
    cart = Cart(request)
    response = {
        'total_len': len(cart),
        'total': cart.get_total_price()
    }
    if product_id:
        product = cart.cart[product_id]
        total_item = int(product['quantity']) * Decimal(product['price'])
        response['total_item'] = total_item
    return JsonResponse(response)
