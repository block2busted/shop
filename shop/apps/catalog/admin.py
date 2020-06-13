from django.contrib import admin
from django.contrib.postgres.fields import JSONField
from .models import Product, Category, Brand, Review
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin, TreeRelatedFieldListFilter
from .utils import ReadableJSONFormField


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass

@admin.register(Product)
class ExampleAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {'form_class': ReadableJSONFormField},
    }


#admin.site.register(Category, DraggableMPTTAdmin)
@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    formfield_overrides = {
        JSONField: {'form_class': ReadableJSONFormField},
    }


@admin.register(Review)
class RatingAdmin(admin.ModelAdmin):
    pass