from django.db import models
from pytils.translit import slugify

class Category(models.Model):
    name = models.TextField(max_length=55, help_text='Название категории')
    description = models.CharField(max_length=250, help_text='Описание')
    slug = models.SlugField(unique=True, max_length=100, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.TextField(max_length=55, unique=True, help_text='Название')
    description = models.CharField(max_length=250, help_text='Описание')
    price = models.IntegerField('Цена')
    photo = models.ImageField('Фото', blank=True, null=True)
    in_stock = models.BooleanField(default=True, help_text='Наличие')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text='Категория')
    slug = models.SlugField(unique=True, max_length=100, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        pass

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)