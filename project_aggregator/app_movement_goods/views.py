from decimal import Decimal

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import TemplateView

from app_catalog.models import Product
from .forms import CartAddProductForm
from .models import UserCart
from .cart import get_cart


@require_POST
def cart_add(request, pk):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=pk)
    form = CartAddProductForm(request.POST)
    # print(form)
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
        # cart_dict = {}
        # for item in cart:
        #     item['update_quantity_form'] = CartAddProductForm()
        #     print(f'item={item}')
        context['cart'] = cart
        # context['cart_dict'] = cart_dict
        return context

    """
    initial={'quantity': item['quantity'], 'update': True}
    КартДетал до цикла корзина= {'use_db': False, 'cart': {'21': {'quantity': 3, 'price': '3299.00'}}, 'user': <SimpleLazyObject: <django.contrib.auth.models.AnonymousUser object at 0x000001DF11EA0D60>>, 'session': <django.contrib.sessions.backends.db.SessionStore object at 0x000001DF11C1FC10>, 'qs': None}
цикл item= {'quantity': 3, 'price': Decimal('3299.00'), 'product': <Product: 3.97" Смартфон BQ 4030G Nice Mini 16 ГБ золотистый>, 'total_price': Decimal('9897.00')}
КартДетал после цикла корзина= {'use_db': False, 'cart': {'21': {'quantity': 3, 'price': Decimal('3299.00'), 'product': <Product: 3.97" Смартфон BQ 4030G Nice Mini 16 ГБ золотистый>, 'total_price': Decimal('9897.00'), 'update_quantity_form': <CartAddProductForm bound=False, valid=Unknown, fields=(quantity;update)>}}, 'user': <SimpleLazyObject: <django.contrib.auth.models.AnonymousUser object at 0x000001DF11EA0D60>>, 'session': <django.contrib.sessions.backends.db.SessionStore object at 0x000001DF11C1FC10>, 'qs': None}

    """


"""
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        ctx['cart'] = cart
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})

        return ctx
"""


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
