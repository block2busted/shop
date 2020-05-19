from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.views.generic import TemplateView, ListView, DetailView
from .models import Product, Category, Subcategory


class IndexView(TemplateView):
    template_name = 'index.html'


class ProductListView(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['product_list'] = Product.objects.all().order_by('name')
        return context


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'catalog/product_detail.html'

    def get_queryset(self):
        queryset = super(ProductDetailView, self).get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super(ProductDetailView, self).get_context_data(**kwargs)
        return context_data


class CategoryListView(ListView):
    model = Category
    template_name = 'catalog/category_list.html'


class SubcategoryListView(DetailView):
    model = Category
    template_name = 'catalog/subcategory_list.html'
    context_object_name = 'category'

    def get_queryset(self):
        return super(SubcategoryListView, self).get_queryset()

    def get_context_data(self, **kwargs):
        context = super(SubcategoryListView, self).get_context_data(**kwargs)
        subcategory_list = Subcategory.objects.filter(category__slug=self.object.slug)
        context['subcategory_list'] = subcategory_list
        return context

