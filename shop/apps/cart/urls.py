from django.urls.conf import path
from .views import add_to_cart, \
    remove_from_cart, \
    reduse_amount, \
    increase_amount,\
    AddCoupon, \
    CartView, \
    CheckoutView, \
    StripePaymentView, \
    PaymentSuccessView, \
    PaymentRobokassaView, \
    YandexPaymentView, \
    login_or_guest, \
 YandexNotifications


app_name = 'cart'
urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add-to-cart/<slug>', add_to_cart, name='add-to-cart'),
    path('add-coupon', AddCoupon.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>', remove_from_cart, name='remove-from-cart'),
    path('reduse-amount/<slug>', reduse_amount, name='reduse-amount'),
    path('increase-amount/<slug>', increase_amount, name='increase-amount'),
    path('checkout', CheckoutView.as_view(), name='checkout'),
    path('payment', StripePaymentView.as_view(), name='payment-stripe'),
    #path('robokassa', PaymentRobokassaView.as_view(), name='payment-robokassa'),
    path('payment-success', PaymentSuccessView.as_view(), name='payment-success'),
    path('authentitication', login_or_guest, name='authentitication'),
    path('payment-yandex', YandexPaymentView.as_view(), name='payment-yandex'),
    path('payment-yandex/notifications', YandexNotifications.as_view(), name='payment-yandex-notifications')
]