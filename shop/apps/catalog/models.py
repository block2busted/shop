from django.db import models
from django.urls import reverse
from pytils.translit import slugify
from mptt.models import MPTTModel, TreeForeignKey

"""class Category(models.Model):
    name = models.CharField(max_length=55, unique=True, help_text='Название категории')
    description = models.TextField(blank=True, help_text='Описание')
    slug = models.SlugField(unique=True, max_length=100, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:subcategory-list', kwargs={'category_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Subcategory(models.Model):
    name = models.CharField(max_length=55, help_text='Подкатегория')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text='Категория')
    description = models.TextField(help_text='Описание', blank=True)
    slug = models.SlugField(unique=True, max_length=100, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Subcategory, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:subcategory-list', kwargs={'slug': self.category.slug})

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'"""


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


class Product(models.Model):
    name = models.CharField(max_length=55, unique=True, help_text='Название')
    description = models.TextField(help_text='Описание')
    price = models.IntegerField('Цена')
    photo = models.ImageField('Фото', default="default.jpg", blank=True, null=True)
    in_stock = models.BooleanField(default=True, help_text='Наличие')
    #subcategory = models.ForeignKey(Subcategory, default='', on_delete=models.CASCADE, blank=True, help_text='Категория')
    slug = models.SlugField(unique=True, max_length=100, blank=True)
    category = TreeForeignKey(Category, on_delete=models.SET_NULL, default='', null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:product-detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
