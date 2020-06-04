from django.db import models
from django.urls import reverse
from mptt.fields import TreeManyToManyField
from pytils.translit import slugify
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField(unique=True, max_length=100, blank=True)
    photo = models.ImageField('Фото', default='default.jpg', blank=True, null=True)

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
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True)
    category = TreeManyToManyField(Category, default=None, blank=True)
    description = models.TextField(help_text='Описание')
    price = models.IntegerField('Цена')
    discount_price = models.IntegerField('Цена со скидкой', blank=True, null=True)
    photo = models.ImageField('Фото', default="default.jpg", blank=True, null=True)
    in_stock = models.BooleanField(default=True, help_text='Наличие')
    slug = models.SlugField(unique=True, max_length=100, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
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
