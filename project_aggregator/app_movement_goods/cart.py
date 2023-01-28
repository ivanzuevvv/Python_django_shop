from .models import UserCart


def get_cart(request):
    # print("session=", request.session.__dict__)
    user = request.user
    session = request.session.session_key
    # print('session_key=', session)
    if not session:
        request.session.cycle_key()
        session = request.session.session_key
        # print('создали session_key=', session)
    data = UserCart.objects.prefetch_related('contents__product').get_or_create(session=session)[0]
    if user.is_authenticated:
        cart = UserCart.objects.prefetch_related('contents__product').get_or_create(owner=user)[0]
        cart.add_cart(data)
    else:
        cart = data
    # print('словарь корзины=', cart.__dict__)
    return cart
