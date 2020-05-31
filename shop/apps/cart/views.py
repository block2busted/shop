from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from catalog.models import Product
from django.views.generic import DetailView
from django.views.generic.base import View
from .models import Order, OrderProduct, Addressee, ShippingAddress
from .forms import CheckoutForm
from django.conf import settings
import stripe


stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"


def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.user.is_authenticated:
        order_queryset = Order.objects.filter(
            user=request.user,
            is_ordered=False
        )
        if order_queryset.exists():
            order = order_queryset[0]
            #order_pk = request.session['order_pk']
            request.session['order_pk'] = order.pk
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
    else:
        try:
            order_pk = request.session['order_pk']
            #order = Order.objects.get(pk=order_pk)
        except:
            order_pk = None
        order = Order.objects.get(pk=order_pk)
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
        order_pk = request.session['order_pk']
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
        order_pk = request.session['order_pk']
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


class CartView(View):
    def get(self, *args, **kwargs):
        try:
            try:  # Если пользователь не залогинен, необходимо доставать его корзину по ключу 'order_pk, если он есть
                order_pk = self.request.session['order_pk']
            except:
                order_pk = None
            #if self.request.user.is_authenticated:
                #Order.objects.filter(pk=order_pk, is_ordered=False).update(user=self.request.user)
                #OrderProduct.objects.filter(order_pk=order_pk, is_ordered=False).update(user=self.request.user)
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
            return render(
                self.request,
                'cart/cart.html',
                context
            )


class CheckoutView(View):
    def get(self, *args, **kwargs):
        order_pk = self.request.session['order_pk']
        order = Order.objects.get(pk=order_pk, is_ordered=False)
        form = CheckoutForm()
        context = {
            'order': order,
            'form': form
        }
        return render(
            self.request,
            'cart/checkout.html',
            context
        )

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        order_pk = self.request.session['order_pk']
        try:
            order = Order.objects.get(pk=order_pk, is_ordered=False)
            if form.is_valid():
                city = form.cleaned_data.get('city')
                street = form.cleaned_data.get('street')
                house = form.cleaned_data.get('house')
                flat = form.cleaned_data.get('flat')
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                email = form.cleaned_data.get('email')
                phone = form.cleaned_data.get('phone')
                if self.request.user.is_authenticated:
                    shipping_address = ShippingAddress(
                        user = self.request.user,
                        city=city,
                        street=street,
                        house=house,
                        flat=flat,
                        order_pk=order_pk,
                    )
                    shipping_address.save()
                    addressee = Addressee(
                        user=self.request.user,
                        order_pk=order_pk,
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        phone=phone
                    )
                else:
                    shipping_address = ShippingAddress(
                        city=city,
                        street=street,
                        house=house,
                        flat=flat,
                        order_pk=order_pk,
                    )
                    shipping_address.save()
                    addressee = Addressee(
                        order_pk=order_pk,
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        phone=phone
                    )
                addressee.save()
                order.shipping_address = shipping_address
                order.addressee = addressee
                order.save()
                return redirect('cart:payment')
        except ObjectDoesNotExist:
            context = {'empty': True}
            return render(
                self.request,
                'cart/cart.html',
                context
            )


class PaymentView(View):
    def get(self, *args, **kwargs):
        return render(
            self.request,
            'cart/payment.html'
        )

    def post(self, *args, **kwargs):
        token = self.request.POST.get('stripeToken')
        stripe.Charge.create(
            amount=2000,
            currency="rub",
            source=token,
            description="My First Test Charge (created for API docs)",
        )
