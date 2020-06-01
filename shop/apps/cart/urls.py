from django.urls.conf import path
from .views import add_to_cart, \
    remove_from_cart, \
    reduse_products_in_cart, \
    increase_products_in_cart,\
    AddCoupon, \
    CartView, \
    CheckoutView, \
    PaymentView


app_name = 'cart'
urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add-to-cart/<slug>', add_to_cart, name='add-to-cart'),
    path('add-coupon', AddCoupon.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>', remove_from_cart, name='remove-from-cart'),
    path('reduse-products-in-cart/<slug>', reduse_products_in_cart, name='reduse-products-in-cart'),
    path('increase-products-in-cart/<slug>', increase_products_in_cart, name='increase-products-in-cart'),
    path('checkout', CheckoutView.as_view(), name='checkout'),
    path('payment', PaymentView.as_view(), name='payment')
]