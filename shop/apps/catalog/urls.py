from django.urls import path
from .views import ProductListView, ProductDetailView, CategoryListView, SubcategoryListView


app_name = 'catalog'
urlpatterns = [
    path('', CategoryListView.as_view(), name='category-list'),
    path('<slug>/', SubcategoryListView.as_view(), name='subcategory-list')

]