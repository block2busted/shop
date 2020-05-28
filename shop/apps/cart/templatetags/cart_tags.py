from django import template
from cart.models import Order

register = template.Library()


@register.filter
def get_cart_product_count(user):
    if user.is_authenticated:
        order_queryset = Order.objects.filter(user=user, is_ordered=False)
        total_product_quantity = 0
        if order_queryset.exists():
            order = order_queryset[0]
            for order_product in order.products.all():
                total_product_quantity += order_product.quantity
    return total_product_quantity


@register.filter
def get_total_order_price(user):
    order_queryset = Order.objects.filter(
        user=user,
        is_ordered=False
    )
    order = order_queryset[0]
    total_order_price = 0
    for order_product in order.products.all():
        total_order_price += order_product.get_final_price()
    return total_order_price
