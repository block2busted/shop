from django.shortcuts import render
# Create your views here.
from django.views.generic import TemplateView, ListView, DetailView
from .models import Product, Category

class IndexView(TemplateView):
    template_name = 'index.html'


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'


class ProductDetailView(DetailView):
    pass