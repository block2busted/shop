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
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

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

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказах'


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    city = models.CharField(max_length=100, help_text='Город')
    street = models.CharField(max_length=100, help_text='Улица')
    house = models.CharField(max_length=100, help_text='Дома')
    flat = models.CharField(max_length=100, help_text='Квартира')
    order_pk = models.IntegerField()

    def __str__(self):
        return f'Адрес заказа №{self.order_pk}'

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'


class Addressee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=100, help_text='Имя')
    last_name = models.CharField(max_length=100, help_text='Фамилия')
    phone = models.CharField(max_length=100, help_text='Телефон')
    email = models.CharField(max_length=100, help_text='Почта')
    order_pk = models.IntegerField()

    def __str__(self):
        return f'Получатель заказа №{self.order_pk}'

    class Meta:
        verbose_name = 'Адресат'
        verbose_name_plural = 'Адресаты'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order_pk = models.IntegerField()
    amount = models.FileField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Оплата заказа №{self.order_pk}'

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.IntegerField()

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    products = models.ManyToManyField(OrderProduct)
    created = models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, blank=True, null=True, default='',
                                         help_text='Адрес доставки')
    addressee = models.ForeignKey(Addressee, on_delete=models.SET_NULL, blank=True, null=True, default='',
                                  help_text='Адресат')
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'Заказ №{self.pk}'

    def get_total_order_price(self):
        total_order_price = 0
        for order_product in self.products.all():
            total_order_price += order_product.get_final_price()
        if self.coupon:
            total_order_price -= total_order_price * self.coupon.amount // 100
        return total_order_price

    def get_total_product_quantity(self):
        total_product_quantity = 0
        for order_product in self.products.all():
            total_product_quantity += order_product.quantity
        return total_product_quantity

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
