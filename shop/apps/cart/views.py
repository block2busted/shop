from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from catalog.models import Product
from django.template.loader import render_to_string
from django.views.generic.base import View, TemplateView
from requests import Response
from robokassa.forms import RobokassaForm
from allauth.account.forms import LoginForm
from .models import Order, OrderProduct, Addressee, ShippingAddress, OrderPayment, Coupon
from .forms import CheckoutForm, CouponForm
import stripe
from yandex_checkout import Configuration, Payment
import uuid
import json

from .services import get_or_create_order_object, \
    _add_product_to_cart, get_order_object, \
    get_order_pk_from_session, \
    _remove_product_from_cart, _reduce_product_quantity, _increase_product_quantity


def add_product_to_cart(request, slug):
    """Добавляет товар в корзину"""
    product = get_object_or_404(Product, slug=slug)
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    order, order_pk = get_or_create_order_object(
        request=request,
        user=user,
        is_ordered=False
    )
    _add_product_to_cart(
        product=product,
        user=user,
        order_pk=order_pk,
        is_ordered=False,
        order=order
    )
    data = {
        'reload_cart': render_to_string('cart/cart_detail.html', {
            'request': request,
        })
    }
    return JsonResponse(data)


def remove_product_from_cart(request, slug):
    """Удаляем товар из корзины"""
    product = get_object_or_404(Product, slug=slug)
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    order_pk = get_order_pk_from_session(request)
    _remove_product_from_cart(
        product=product,
        user=user,
        order_pk=order_pk,
        is_ordered=False
    )
    return redirect('cart:cart')


def reduce_amount(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    _reduce_product_quantity(
        product,
        user,
        order_pk=get_order_pk_from_session(request),
        is_ordered=False
    )
    return redirect('cart:cart')


def increase_amount(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    _increase_product_quantity(
        product,
        user,
        order_pk=get_order_pk_from_session(request),
        is_ordered=False
    )
    return redirect('cart:cart')


def login_or_guest(request):
    form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'cart/login_or_guest.html', context)


class CartView(View):
    def get(self, *args, **kwargs):
        try:
            try:  # Если пользователь не залогинен, необходимо доставать его корзину по ключу 'order_pk, если он есть
                order_pk = self.request.session['order_pk']
            except:
                order_pk = None
            order = Order.objects.get(pk=order_pk, is_ordered=False)
            order_product = OrderProduct.objects.filter(order_pk=order_pk, is_ordered=False).order_by('-created')
            context = {
                'order': order,
                'order_product': order_product
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


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, 'Промокод не найден')
        order_pk = request.session['order_pk']
        order = Order.objects.get(pk=order_pk, is_ordered=False)
        form = CheckoutForm()
        coupon_form = CouponForm(request.POST or None)
        context = {
            'order': order,
            'coupon_form': coupon_form,
            'form': form,
        }
        return render(
            request,
            'cart/checkout.html',
            context)


class AddCoupon(View):
    def post(self, *args, **kwargs):
        coupon_form = CouponForm(self.request.POST or None)
        form = CheckoutForm()
        if coupon_form.is_valid():
            try:
                code = coupon_form.cleaned_data.get('code')
                order_pk = self.request.session['order_pk']
                order = Order.objects.get(pk=order_pk, is_ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                context = {
                    'order': order,
                    'coupon_form': CouponForm(),
                    'form': form
                }
                messages.success(self.request, 'Вы использовали промокод')
                return render(
                    self.request,
                    'cart/checkout.html',
                    context
                )
            except ObjectDoesNotExist:
                messages.info(self.request, 'У вас нет активных заказов')
                return render(self.request, 'cart/checkout.html')
        return None


class CheckoutView(View):
    def get(self, *args, **kwargs):
        order_pk = self.request.session['order_pk']
        order = Order.objects.get(pk=order_pk, is_ordered=False)
        form = CheckoutForm()
        context = {
            'order': order,
            'coupon_form': CouponForm(),
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
                payment_option = form.cleaned_data.get('payment_option')
                if self.request.user.is_authenticated:
                    shipping_address = ShippingAddress(
                        user=self.request.user,
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
                if payment_option == 'S':
                    return redirect('cart:payment-stripe')
                elif payment_option == 'H':
                    return redirect('cart:payment-success')
                elif payment_option == 'Y':
                    return redirect('cart:payment-yandex')
        except ObjectDoesNotExist:
            context = {'empty': True}
            return render(
                self.request,
                'cart/cart.html',
                context
            )


class StripePaymentView(View):
    def get(self, *args, **kwargs):
        return render(
            self.request,
            'cart/payment_stripe.html'
        )

    def post(self, *args, **kwargs):
        order_pk = self.request.session['order_pk']
        order = Order.objects.get(pk=order_pk, is_ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = order.get_total_order_price()
        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency="rub",
                source=token,
            )
            # Создаём payment
            payment = OrderPayment()
            payment.stripe_charge_id = charge['id']
            payment.order_pk = order_pk
            if self.request.user.is_authenticated:
                payment.user = self.request.user
            payment.amount = amount
            payment.save()
            # Добавляем оплату к заказу
            order_products = order.products.all()
            order_products.update(is_ordered=True)
            for product in order_products:
                product.save()
            order.is_ordered = True
            order.payment = payment
            order.save()
            messages.success(self.request, 'Ваш заказ оплачен.')
            return redirect('/')
        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.error(self.request, f"{err.get('message')}")
            return redirect('/')
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(self.request, 'Invalid parameters!')
            return redirect('/')
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(self.request, '')
            return redirect('/')
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(self.request, 'Not authenticated!')
            return redirect('/')
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(self.request, 'Network error!')
            return redirect('/')
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(self.request, 'Что-по пошло не так, оплата не прошла!')
            return redirect('/')
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            messages.error(self.request, 'Что-то не так')
            return redirect('/')


class PaymentRobokassaView(View):
    def get(self, *args, **kwargs):
        order_pk = self.request.session['order_pk']
        order = Order.objects.get(pk=order_pk, is_ordered=False)
        amount = order.get_total_order_price()
        print(amount)
        form = RobokassaForm(initial={
            'OutSum': amount,
            'InvId': order_pk,
            'Desc': 'Тестовая оплата',
            'IsTest': 1,
            'MerchantLogin': 'BlockbustedShop',
            'Pass1': 's6pS1LpEhZO0m6iWHT4i',
            'SignatureValue': 'U4aTMmo8mF4dIhHP5hJ9',
        })
        context = {
            'form': form,
        }
        return render(self.request, 'cart/payment_robokassa.html', context)

    def post(self, *args, **kwargs):
        order_pk = self.request.session['order_pk']
        order = Order.objects.get(pk=order_pk, is_ordered=False)
        amount = order.get_total_order_price()
        print(amount)
        form = RobokassaForm(initial={
            'OutSum': amount,
            'InvId': order_pk,
            'Desc': 'Тестовая оплата',
            'IsTest': 1,
            'MerchantLogin': 'BlockbustedShop',
            'Pass1': 's6pS1LpEhZO0m6iWHT4i',
            'SignatureValue': 'U4aTMmo8mF4dIhHP5hJ9',
        })
        context = {
            'form': form,
        }
        return render(self.request, 'cart/payment_robokassa.html', context)


class PaymentSuccessView(TemplateView):
    template_name = 'cart/payment_success.html'


class YandexPaymentView(View):
    def get(self, request):
        with open('/Users/blockbusted/PycharmProjects/config_shop_file.json') as config_file:
            config = json.load(config_file)
        Configuration.account_id = config['YANDEX_SHOP_ID']
        Configuration.secret_key = config['YANDEX_SECRET_KEY']

        order_pk = self.request.session['order_pk']
        order = Order.objects.get(pk=order_pk)
        amount = order.get_total_order_price()
        idempotence_key = str(uuid.uuid4())
        payment = Payment.create({
            #  "payment_token": idempotence_key,
            "amount": {
                "value": 1,
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "cart:payment-yandex-notifications"
            },
            "description": "Заказ №"+str(order_pk)
        })

        order_payment = OrderPayment()
        order_payment.order_pk = order_pk
        if self.request.user.is_authenticated:
            order_payment.user = self.request.user
        order_payment.amount = amount
        order_payment.save()
        return HttpResponseRedirect(payment.confirmation.confirmation_url)


class YandexNotifications(View):
    def get(self, request):
        order_pk = request.session['order_pk']
        order_payment = OrderPayment.objects.get(order_pk=order_pk)
        payment_id = request.data['object']['id']
        Payment.capture(payment_id)
        order = Order.objects.get(pk=order_pk)
        order_products = order.products.all()
        order_products.update(is_ordered=True)
        for product in order_products:
            product.save()
        order.is_ordered = True
        #order.payment = payment
        order.payment.charge_id = payment_id
        order.save()
        return Response(status=200)