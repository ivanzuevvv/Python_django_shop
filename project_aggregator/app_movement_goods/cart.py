from .models import UserCart


def get_cart(request):
    user = request.user
    session = request.session.session_key
    if not session:
        request.session.cycle_key()
        session = request.session.session_key
    data = UserCart.objects.get_or_create(session=session)
    print('cart', data)
    if user.is_authenticated:
        cart = UserCart.objects.get_or_create(owner=user)[0]
        cart.add_cart(data[0])
    else:
        cart = data[0]
    return cart

