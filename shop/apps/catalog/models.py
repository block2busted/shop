from django.db import models
from django.urls import reverse
from mptt.fields import TreeManyToManyField
from pytils.translit import slugify
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.postgres.fields import JSONField
from django.conf import settings


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField(unique=True, max_length=100, blank=True)
    photo = models.ImageField('Фото', default='default.jpg', blank=True, null=True)
    attributes = JSONField(default=dict, help_text='Характеристики')
    filters = JSONField(default=dict, help_text='Фильтр по динамичесим атрибутам')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text='Название')
    description = models.TextField(help_text='описание', blank=True)
    photo = models.ImageField('Фото', default='default.jpg', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'


class Product(models.Model):
    name = models.CharField(max_length=55, unique=True, help_text='Название')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True, help_text='Бренд')
    category = TreeForeignKey(Category, on_delete=models.SET_NULL, default=None, blank=True, null=True, help_text='Категория')
    description = models.TextField(help_text='Описание')
    price = models.IntegerField('Цена')
    discount_price = models.IntegerField('Цена со скидкой', blank=True, null=True, help_text='Цена со скидкой')
    photo = models.ImageField('Фото', default="default.jpg", blank=True, null=True)
    in_stock = models.BooleanField(default=True, help_text='Наличие')
    slug = models.SlugField(unique=True, max_length=100, blank=True)
    attributes = JSONField(default=dict, help_text='Характеристики', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        #print(self.attributes)
        #if self.attributes == dict:
        if len(str(self.attributes)) <= 2:
            self.attributes = self.category.attributes
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:product-detail', kwargs={'slug': self.slug})

    def get_discount(self):
        discount = int(self.price)-int(self.discount_price)
        return discount

    def get_add_to_cart_url(self):
        return reverse('cart:add-to-cart', kwargs={'slug': self.slug})

    def get_remove_from_cart_url(self):
        return reverse('cart:remove-from-cart', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        #ordering = ['-price']


RATING_CHOISE = (
    ('1 звезда', 'Ужасно'),
    ('2 звезды', 'Не нравится'),
    ('3 звезды', 'Нормально'),
    ('4 звезды', 'Хорошо'),
    ('5 звёзд', 'Великолепно')
)


RECOMEND_CHOICE = (
    ('Y', 'Да'),
    ('N', 'Нет')
)


class Review(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text='Автор отзыва')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, help_text='Товар')
    rating = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    is_recommend = models.BooleanField(default=False)
    plus = models.CharField(default='', max_length=255, blank=True, null=True, help_text='Плюсы')
    minus = models.CharField(default='', max_length=255, blank=True, null=True, help_text='Минусы')
    content = models.TextField(default='', max_length=400,help_text='Отзыв')
    photo = models.ImageField(upload_to='catalog/review', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('catalog:product-detail', kwargs={'slug': self.product.slug})
