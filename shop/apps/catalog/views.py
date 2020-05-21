from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from .models import Product, Category


class IndexView(TemplateView):
    template_name = 'index.html'


class CategoryListView(ListView):
    template_name = "catalog/category_list.html"
    model = Category

    def get_queryset(self):
        queryset = super(CategoryListView, self).get_queryset()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView, self).get_context_data()
        category_roots = Category.objects.filter(parent=None)
        categories = category_roots.get_descendants(include_self=True)
        context['categories'] = categories
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'catalog/category_detail.html'

    def get_queryset(self):
        queryset = super(CategoryDetailView, self).get_queryset()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryDetailView, self).get_context_data()
        category_list = Category.objects.filter(parent__slug=self.object.slug)
        context['category_list'] = category_list
        return context



class ProductListView(DetailView):
    model = Category
    template_name = 'catalog/product_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data()
        product_list = Product.objects.filter(category__slug=self.object.slug)
        context['product_list'] = product_list
        return context
