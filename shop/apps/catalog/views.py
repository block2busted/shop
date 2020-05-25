from django.db.models import Q, Count
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
        category_roots = Category.objects.filter(parent__slug=self.object.slug)
        category_list = category_roots.get_descendants(include_self=True)
        context['category_list'] = category_list
        context['category_roots'] = category_roots
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    paginate_by = 12
    context_object_name = 'product_list'

    def get_queryset(self):
        queryset = super(ProductListView, self).get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data()
        category = Category.objects.get(slug=self.kwargs['slug'])
        context['category'] = category
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        queryset = super(ProductDetailView, self).get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        product = get_object_or_404(Product, slug=self.object.slug)
        context['product'] = product
        return context


class SearchResultsView(ListView):
    model = Product
    template_name = 'catalog/search_results.html'
    context_object_name = 'product_list'
    paginate_by = 12

    def get_queryset(self):
        queryset = super(SearchResultsView, self).get_queryset()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchResultsView, self).get_context_data()
        queryset = self.request.GET.get('queryset')
        product_list = Product.objects.filter(
            Q(name__icontains=queryset)
        )
        context['product_list'] = product_list
        context['total_products'] = product_list.count()
        return context


