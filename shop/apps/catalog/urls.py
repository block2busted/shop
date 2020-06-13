from django.urls import path
from .views import CategoryListView, \
    CategoryDetailView, \
    ProductListView, \
    ProductDetailView, \
    ReviewCreateView


app_name = 'catalog'
urlpatterns = [
    path('', CategoryListView.as_view(), name='category-list'),
    path('<slug>', CategoryDetailView.as_view(), name='category-detail'),
    path('<slug>/products/', ProductListView.as_view(), name='product-list'),
    path('product/<slug>', ProductDetailView.as_view(), name='product-detail'),
    path('product/<slug>/review-create', ReviewCreateView.as_view(), name='review-create'),

]