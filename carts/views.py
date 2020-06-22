from django.shortcuts import render, redirect
from django.http import JsonResponse

from orders.models import Order

from accounts.forms import LoginForm, GuestForm
from addresses.forms import AddressForm
from addresses.models import Address
from .models import Cart

from products.models import Product
from billing.models import BillingProfile


# Create your views here.


def cart_detail_api_view(request):
    cart_object, new_object = Cart.objects.new_or_getcurrent(request)
    products = [
        {
         'object_title': obj.title,
         'object_price': obj.price,
         'url': obj.get_absolute_url(),
         'id': obj.id
         }
        for obj in cart_object.products.all()]
    cart_data = {'products': products, 'subtotal': cart_object.subtotal, 'total': cart_object.total}

    return JsonResponse(cart_data)


def cart(request):
    cart_object, new_object = Cart.objects.new_or_getcurrent(request)
    context = {
        'cart': cart_object
    }
    return render(request, 'index.html', context)


def cart_update(request):
    print(request.POST)
    product_added = True
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect('cart')
        cart_object, new_object = Cart.objects.new_or_getcurrent(request)
        if product in cart_object.products.all():
            cart_object.products.remove(product)
            product_added = False
        else:
            cart_object.products.add(product)
            request.session['cart_items'] = cart_object.products.count()
            product_added = True

        if request.is_ajax():
            print('This Is An Ajax Request....')
            json_data = {
                'productAdded': product_added,
                'productRemoved': not product_added,
                'CartItemCount': cart_object.products.count(),
            }

            return JsonResponse(json_data)

    return redirect('cart')


def checkout(request):
    cart_object, new_cart_object = Cart.objects.new_or_getcurrent(request)
    order_object = None
    if new_cart_object or cart_object.products.count() == 0:
        return redirect('cart')

    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_form = AddressForm()
    billing_address_id = request.session.get('billing_address_id', None)
    shipping_address_id = request.session.get('shipping_address_id', None)

    address_qs = None
    has_card = False

    billing_profile, billing_profile_created = BillingProfile.objects.get_or_create_billing_profile(request)
    if billing_profile is not None:
        if request.user.is_authenticated():
            address_qs = Address.objects.filter(billing_profile=billing_profile)

        order_object, order_object_created = Order.objects.get_or_create_order(billing_profile, cart_object)
        if shipping_address_id:
            order_object.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
        if billing_address_id:
            order_object.billing_address = Address.objects.get(id=billing_address_id)
            del request.session['billing_address_id']
        if shipping_address_id or billing_address_id:
            order_object.save()

        has_card = billing_profile.has_card()

    if request.method == 'POST':
        order_completed = order_object.order_complete()
        if order_completed:
            did_charge, charge_message = billing_profile.charge(order_object)
            if did_charge:
                order_object.mark_paid()
                del request.session['cart_id']
                request.session['cart_items'] = 0
                return redirect('success')
            else:
                print(charge_message)
                redirect('checkout')

    context = {
        'order': order_object,
        'billing_profile': billing_profile,
        'login_form': login_form,
        'guest_form': guest_form,
        'address_form': address_form,
        'billing_address_form': billing_address_form,
        'address_qs': address_qs,
        'has_card': has_card,
        'public_key': public_key,
    }
    return render(request, 'checkout.html', context)


def checkout_complete(request):
    return render(request, 'checkout_success.html')
