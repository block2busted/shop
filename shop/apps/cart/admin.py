from django.contrib import admin
from .models import OrderProduct, Order, ShippingAddress, Addressee
# Register your models here.


admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(ShippingAddress)
admin.site.register(Addressee)
