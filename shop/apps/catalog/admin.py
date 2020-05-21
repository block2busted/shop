from django.contrib import admin
from .models import Product, Category
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'description', 'in_stock', 'price', 'photo', 'slug']


admin.site.register(Category, DraggableMPTTAdmin)
