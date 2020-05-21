from django.urls import path
from .views import CategoryListView, CategoryDetailView, ProductListView

app_name = 'catalog'
urlpatterns = [
    #path('', CategoryListView.as_view(), name='category-list'),
    path('<slug>', CategoryDetailView.as_view(), name='category-detail'),
    path('<slug>/products/', ProductListView.as_view(), name='product-list')

]