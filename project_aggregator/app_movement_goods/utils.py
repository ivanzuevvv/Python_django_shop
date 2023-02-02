import json
import time

import requests
from django.db import IntegrityError, transaction
from requests import ConnectTimeout, HTTPError, ReadTimeout, Timeout

from app_catalog.models import Product
from app_configurations.models import SiteSettings
from .models import Order


def get_payment_status(card_number: int):
    post_data = {'card_number': card_number}
    response = requests.post("http://127.0.0.1:8000/payment/new/", data=post_data, timeout=10)
    response.raise_for_status()
    content = response.content
    result = json.loads(content.decode('utf-8'))
    return result['status'], result['code']


def get_delivery_price(total, type_delivery):
    settings = SiteSettings.load()
    usual_delivery_price = settings.cost_usual_delivery
    edge_delivery = settings.min_cost_for_free_delivery
    express_delivery_price = settings.cost_express_delivery
    if type_delivery == '2':
        return express_delivery_price
    if total < edge_delivery:
        return usual_delivery_price
    else:
        return 0


def order_created(order_id):
    # time.sleep(5)
    order = Order.objects.get(id=order_id)
    status = ''
    payment_code = order.payment_code
    objs_store = []
    try:
        for item in order.items.all():
            store_good = Product.objects.select_for_update().get(id=item.product.id)
            if item.quantity > store_good.stock:
                status = f'{item.product.name} недостаточно на складе'
                raise IntegrityError
            store_good.stock -= item.quantity
            objs_store.append(store_good)
        with transaction.atomic():
            if payment_code != 1:
                Product.objects.bulk_update(objs_store, ['stock'])
                status, payment_code = get_payment_status(order.card_number)
                if payment_code == 1:
                    order.paid = True
                else:
                    raise IntegrityError
    except IntegrityError:
        payment_code = 2
    except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError):
        payment_code = 3
        status = "Нет связи с сервером оплаты"

    order.status = status
    order.payment_code = payment_code
    order.save()
