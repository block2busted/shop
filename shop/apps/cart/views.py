from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from catalog.models import Product
from django.views.generic import DetailView
from django.views.generic.base import View

from .models import Order, OrderProduct


def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.user.is_authenticated:
        order_queryset = Order.objects.filter(
            user=request.user,
            is_ordered=False
        )
        if order_queryset.exists():
            order = order_queryset[0]
            order_pk = request.session['order_pk']
            order_product, created = OrderProduct.objects.get_or_create(
                product=product,
                user=request.user,
                order_pk=order_pk,
                is_ordered=False
            )
            if order.products.filter(product__slug=product.slug).exists():
                return redirect('catalog:product-detail', slug)
            else:
                messages.info(request, "Вы добавили товар в корзину.")
                order.products.add(order_product)
                return redirect('catalog:product-detail', slug)
        else:
            order = Order.objects.create(user=request.user)
            order_pk = order.pk
            request.session['order_pk'] = order.pk
            order_product, created = OrderProduct.objects.get_or_create(
                product=product,
                user=request.user,
                order_pk=order_pk,
                is_ordered=False
            )
            order.products.add(order_product)
            messages.info(request, "Вы добавили товар в корзину.")
            return redirect('catalog:product-detail', slug)
    else:
        try:
            order_pk = request.session['order_pk']
            order = Order.objects.get(pk=order_pk)
        except:
            order = Order.objects.create()
            request.session['order_pk'] = order.pk
            order_pk = order.pk
        order_product, created = OrderProduct.objects.get_or_create(
            product=product,
            order_pk=order_pk,
            is_ordered=False
        )
        if order.products.filter(product__slug=product.slug).exists():
            return redirect('catalog:product-detail', slug)
        else:
            messages.info(request, "Вы добавили товар в корзину.")
            order.products.add(order_product)
            return redirect('catalog:product-detail', slug)


'''def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.user.is_authenticated:
        order_product, created = OrderProduct.objects.get_or_create(
            product=product,
            user=request.user,
            is_ordered=False)
        order_queryset = Order.objects.filter(
            user=request.user,
            is_ordered=False
        )
    if order_queryset.exists():
        order = order_queryset[0]
        if order.products.filter(product__slug=product.slug).exists():
            return redirect('catalog:product-detail', slug)
        else:
            messages.info(request, "Вы добавили товар в корзину.")
            order.products.add(order_product)
            return redirect('catalog:product-detail', slug)
    else:
        #order = Order.objects.create(user=request.user)
        order = Order.objects.create(pk=the_pk)
        order.products.add(order_product)

        messages.info(request, "Вы добавили товар в корзину.")
        return redirect('catalog:product-detail', slug)
'''


def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.user.is_authenticated:
        order_queryset = Order.objects.filter(
            user=request.user,
            is_ordered=False
        )
        if order_queryset.exists():
            order = order_queryset[0]
            if order.products.filter(product__slug=product.slug).exists():
                order_product = OrderProduct.objects.filter(
                    product=product,
                    user=request.user,
                    is_ordered=False
                )[0]
                order_product.delete()
                return redirect('cart:cart')
            else:
                messages.info(request, "Товар не добавлен в корзину.")
                return redirect('cart:cart')
        else:
            messages.info(request, "У вас нет активных заказов.")
            return redirect('cart:cart')
        return redirect('cart:cart')
    else:
        try:
            order_pk = request.session['order_pk']
            order = Order.objects.get(pk=order_pk)
        except:
            the_pk = None
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(
                product=product,
                order_pk=order_pk,
                is_ordered=False
            )[0]
            order_product.delete()
            return redirect('cart:cart')
        else:
            messages.info(request, "Товар не добавлен в корзину.")
            return redirect('cart:cart')


class CartView(View, LoginRequiredMixin):
    def get(self, *args, **kwargs):
        try:
            if self.request.user.is_authenticated:
                order = Order.objects.get(user=self.request.user, is_ordered=False)
            else:
                try:  # Если пользователь не залогинен, необходимо доставать его корзину по ключу 'order_pk, если он есть
                    order_pk = self.request.session['order_pk']
                except:
                    order_pk = None
                order = Order.objects.get(pk=order_pk, is_ordered=False)
            context = {
                'order': order
            }
            return render(
                self.request,
                'cart/cart.html',
                context
            )
        except ObjectDoesNotExist:
            context = {'empty': True}
            # messages.error(self.request, 'У вас нет заказов')
            return render(
                self.request,
                'cart/cart.html',
                context
            )


def reduse_products_in_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.user.is_authenticated:
        order_queryset = Order.objects.filter(
            user=request.user,
            is_ordered=False
        )
        if order_queryset.exists():
            order = order_queryset[0]
            if order.products.filter(product__slug=product.slug).exists():
                order_product = OrderProduct.objects.filter(
                    product=product,
                    user=request.user,
                    is_ordered=False
                )[0]
                if order_product.quantity > 1:
                    order_product.quantity -= 1
                    order_product.save()
            else:
                return redirect('cart:cart')
        else:
            messages.info(request, "У вас нет активных заказов.")
            return redirect('cart:cart')
    else:
        try:
            order_pk = request.session['order_pk']
        except:
            order_pk = None
        order = Order.objects.get(pk=order_pk, is_ordered=False)
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(
                product=product,
                order_pk=order_pk,
                is_ordered=False
            )[0]
            if order_product.quantity > 1:
                order_product.quantity -= 1
                order_product.save()
        else:
            return redirect('cart:cart')
    return redirect('cart:cart')


def increase_products_in_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.user.is_authenticated:
        order_queryset = Order.objects.filter(
            user=request.user,
            is_ordered=False
        )
        if order_queryset.exists():
            order = order_queryset[0]
            if order.products.filter(product__slug=product.slug).exists():
                order_product = OrderProduct.objects.filter(
                    product=product,
                    user=request.user,
                    is_ordered=False
                )[0]
                order_product.quantity += 1
                order_product.save()
            else:
                return redirect('cart:cart')
        else:
            messages.info(request, "У вас нет активных заказов.")
            return redirect('cart:cart')
        return redirect('cart:cart')
    else:
        try:
            order_pk = request.session['order_pk']
        except:
            order_pk = None
        order = Order.objects.get(pk=order_pk, is_ordered=False)
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(
                product=product,
                order_pk=order_pk,
                is_ordered=False
            )[0]
            order_product.quantity += 1
            order_product.save()
        else:
            return redirect('cart:cart')
    return redirect('cart:cart')
