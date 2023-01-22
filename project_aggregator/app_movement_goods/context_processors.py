from .models import UserCart
from .session_entities import Cart


# def get_cart(request):
#     if request.user.is_authenticated:
#         if UserCart.objects.filter(owner=request.user).exists():
#             cart = UserCart.objects.create(owner=request.user).content
#         context = {'cart': Cart(request)}
#         return
#
#     context = {'cart': Cart(request)}
#     return context

def get_cart(request):
    if request.user.is_authenticated:
        cart = UserCart.objects.get_or_create(owner=request.user)[0].cart
    else:
        cart = Cart(request).cart

    context = {'cart': cart}
    return context
