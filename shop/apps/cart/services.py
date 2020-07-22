from django.core.exceptions import ObjectDoesNotExist

from .models import Order, OrderProduct


def get_order_object(order_pk, user, is_ordered):
    order = Order.objects.filter(
        pk=order_pk,
        user=user,
        is_ordered=is_ordered
    )[0]
    return order


def get_order_pk_from_session(request):
    try:
        order_pk = request.session['order_pk']
    except:
        order_pk = None
    return order_pk


def get_or_create_order_object(request, user, is_ordered):
    """Получаем из базы данных или создаем заказ"""
    try:
        order_pk = request.session['order_pk']
        order = get_order_object(order_pk=order_pk, user=user, is_ordered=is_ordered)
    except KeyError:
        order = Order.objects.create(user=user, is_ordered=is_ordered)
    request.session['order_pk'] = order.pk
    order_pk = order.pk
    return order, order_pk


def _check_product_to_user_session(order_product, user):
    """Проверяет сессию пользователя. Если у него есть действующий заказ, обновляет
    его, добавляя в него пользователя"""
    if user:
        order_product.user = user
        order_product.save()


def get_or_create_order_product(product, user, order_pk, is_ordered, created):
    if created:
        order_product, created = OrderProduct.objects.get_or_create(
            product=product,
            order_pk=order_pk,
            is_ordered=is_ordered
        )
    else:
        order_product = OrderProduct.objects.get(
            product=product,
            order_pk=order_pk,
            is_ordered=is_ordered
        )
    _check_product_to_user_session(order_product=order_product, user=user)
    return order_product


def _add_product_to_cart(product, user, order_pk, is_ordered, order):
    """Добавляет товар в корзину"""
    order_product = get_or_create_order_product(product, user, order_pk, is_ordered, created=True)
    order.products.add(order_product)


def _remove_product_from_cart(product, user, order_pk, is_ordered):
    order_product = get_or_create_order_product(product, user, order_pk, is_ordered, created=False)
    order_product.delete()


def _reduce_product_quantity(product, user, order_pk, is_ordered):
    order_product = get_or_create_order_product(product, user, order_pk, is_ordered, created=False)
    if order_product.quantity > 1:
        order_product.quantity -= 1
        order_product.save()


def _increase_product_quantity(product, user, order_pk, is_ordered):
    order_product = get_or_create_order_product(product, user, order_pk, is_ordered, created=False)
    order_product.quantity += 1
    order_product.save()
