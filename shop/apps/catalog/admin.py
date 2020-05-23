from django.contrib import admin
from .models import Product, Category, Brand
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin, TreeRelatedFieldListFilter


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, DraggableMPTTAdmin)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass
