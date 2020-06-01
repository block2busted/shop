from django import template
from cart.models import Order, OrderProduct

register = template.Library()


@register.filter
def get_cart_product_count(request):
    total_product_quantity = 0
    try:
        order_pk = request.session['order_pk']
    except:
        order_pk = None
    if order_pk:
        order_queryset = Order.objects.filter(pk=order_pk, is_ordered=False)
        if order_queryset.exists():
            order = order_queryset[0]
            for order_product in order.products.all():
                total_product_quantity += order_product.quantity
    return total_product_quantity


@register.filter
def get_total_order_price(request):
    try:
        order_pk = request.session['order_pk']
    except:
        order_pk = None
    if order_pk:
        total_order_price = 0
        order_queryset = Order.objects.filter(pk=order_pk, is_ordered=False)
        if order_queryset.exists():
            order = order_queryset[0]
            for order_product in order.products.all():
                total_order_price += order_product.get_final_price()
            if order.coupon:
                total_order_price -= total_order_price * (order.coupon.amount) // 100 # Если есть промокод
        else:
            total_order_price = 0
    else:
        total_order_price = 0
    return total_order_price
