from decimal import Decimal

from django.conf import settings

from app_catalog.models import Product
from .models import UserCart


def get_cart(request):
    user = request.user
    session = request.session.get('session_key')
    print(session)
    if not session:
        request.session.cycle_key()
        session = request.session.get('session_key')
        print('session=', session)

    cart = UserCart.objects.get_or_create(session=session)
    print('cart', cart)
    if user.is_authenticated:
        cart = UserCart.objects.get_or_create(owner=user)[0]
    cart_tuple_ano = UserCart.objects.get_or_create(session=session)
    return cart

