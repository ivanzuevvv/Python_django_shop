from .models import UserCart


def get_cart(request):
    print("session=", request.session.__dict__)
    user = request.user
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()
        session_key = request.session.session_key
        print('создали session_key=', session_key)
    if not user.is_authenticated:
        cart = UserCart.objects.prefetch_related('contents__product').get_or_create(session=session_key)[0]
        no_user_cart_id = cart.id
    else:
        print(no_user_cart_id)
        cart = UserCart.objects.prefetch_related('contents__product').get_or_create(owner=user)[0]
        try:
            data = UserCart.objects.prefetch_related('contents__product').get(pk=no_user_cart_id)
        except Exception:
            print('Корзины не было')
        else:
            cart.add_cart(data)
    # print('словарь корзины=', cart.__dict__)
    return cart
