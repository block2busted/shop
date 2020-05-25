from django import template
from cart.models import Order

register = template.Library()

@register.filter
def get_cart_product_count(user):
    if user.is_authenticated:
        order_queryset = Order.objects.filter(user=user, is_ordered=False)
        if order_queryset.exists():
            return order_queryset[0].products.count()
    return 0


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