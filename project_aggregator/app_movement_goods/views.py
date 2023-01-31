from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import FormMixin

from app_catalog.models import Product
from app_configurations.models import SiteSettings
from app_users.forms import RegUserForm
from .forms import CartAddProductForm, OrderCreateForm
from .cart import get_cart
from .models import OrderContents, Order
from .utils import get_delivery_price, order_created


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


class OrderView(FormMixin, TemplateView):
    template_name = 'app_orders/order.html'
    form_class = OrderCreateForm
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_cart(self.request)
        total_cost = cart.get_total_price
        choices = []
        settings = SiteSettings.load()
        usual_delivery_price = settings.cost_usual_delivery
        edge_delivery = settings.min_cost_for_free_delivery
        express_delivery_price = settings.cost_express_delivery
        context['price_usual'] = 0
        if total_cost < edge_delivery:
            choices.append(('1', f'Обычная доставка (+{usual_delivery_price} ₽)'))
            context['price_usual'] = usual_delivery_price
        else:
            choices.append(('1', f'Обычная доставка (бесплатно)'))
        context['total_with_delivery'] = total_cost + get_delivery_price(total=cart.get_total_price,
                                                                         type_delivery='1')
        choices.append(('2', f'Экспресс доставка (+{express_delivery_price} ₽)'))
        context['form'].fields['delivery_type'].widget.choices = choices
        if self.request.user.is_authenticated:
            instance = self.request.user
            context['form_reg'] = RegUserForm(instance=instance)
            context['form_reg'].fields['email'].disabled = True
            context['form_reg'].fields['full_name'].disabled = True
            context['form_reg'].fields['phone'].disabled = True
        else:
            context['form_reg'] = RegUserForm()
        return context

    def post(self, request):
        cart = get_cart(request)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.data = form.cleaned_data
            order.owner = request.user
            order.delivery_price = get_delivery_price(
                total=cart.get_total_price, type_delivery=form.cleaned_data['delivery_type'])
            objs = []
            for item in cart:
                objs.append(
                    OrderContents(
                        order=order, product=item['product'],
                        price=item['price'], quantity=item['quantity']))
            order.save()
            OrderContents.objects.bulk_create(objs)
            cart.clear()
            messages.success(request, 'Заказ успешно добавлен.')
            messages.info(request, 'Ждём подтверждения оплаты от платёжной системы.')
            order_created(order.id)
            return HttpResponseRedirect(reverse('order_detail', args=[order.id]))
        return super().form_invalid(form)


class OrderDetail(LoginRequiredMixin, DetailView):
    template_name = "app_orders/oneorder.html"
    raise_exception = True
    model = Order
    context_object_name = 'order'

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        if object.owner != self.request.user:
            raise PermissionDenied
        return object


class HistoryOrders(LoginRequiredMixin, ListView):
    template_name = "app_orders/historyorder.html"
    raise_exception = True
    model = Order
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = (Order.objects.only(
            'id', 'created_at', 'paid', 'delivery_type', 'payment_type', 'paid', 'status').
            filter(owner=self.request.user))
        return queryset

