from django.db import models
from django.conf import settings
from catalog.models import Product
from django.contrib.auth.models import User


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    order_pk = models.IntegerField(blank=True, null=True, help_text='В каком заказе')
    is_ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'Заказ №{self.order_pk}: {self.product.name} x {self.quantity}'

    def get_total_product_price(self):
        return self.quantity * self.product.price

    def get_total_discount_product_price(self):
        return self.quantity * self.product.discount_price

    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_discount_product_price()
        return self.get_total_product_price()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    products = models.ManyToManyField(OrderProduct)
    created = models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'Заказ №{self.pk}'

    def get_total_order_price(self):
        total_order_price = 0
        for order_product in self.products.all():
            total_order_price += order_product.get_final_price()
        return total_order_price

    def get_total_product_quantity(self):
        total_product_quantity = 0
        for order_product in self.products.all():
            total_product_quantity += order_product.quantity
        return total_product_quantity
