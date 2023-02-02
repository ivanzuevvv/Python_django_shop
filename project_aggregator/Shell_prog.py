import random

from app_movement_goods.models import UserCart
from app_catalog.models import Product, ExtraData, ValueData, TitleData
from app_users.models import User

# user1 = User.objects.get(pk=9)
# user2 = User.objects.get(pk=12)
# prod1 = Product.objects.get(pk=10)
# prod2 = Product.objects.get(pk=15)
# prod3 = Product.objects.get(pk=23)
# cart1 = UserCart.objects.get_or_create(owner=user1)[0]
# cart2 = UserCart.objects.get_or_create(owner=user2)[0]

# all_prod = Product.objects.filter(id__gte=2)
# list_country = ValueData.objects.filter(id__in=[1, 4, 9, 10, 11, 12, 13])  # страны
# list_term = ValueData.objects.filter(id__in=[3, 6, 7, 8])  # сроки
# list_type = ValueData.objects.filter(id__in=[2, 5])  # тип
# list_title = TitleData.objects.all()
# for prod in all_prod:
#     country = random.choice(list_country)
#     term = random.choice(list_term)
#     types = random.choice(list_type)
#     ExtraData.objects.create(title=list_title[0], device=prod, value=country)
#     ExtraData.objects.create(title=list_title[1], device=prod, value=types)
#     ExtraData.objects.create(title=list_title[2], device=prod, value=term)
