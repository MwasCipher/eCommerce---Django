from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import stripe

# Create your views here.
from django.utils.http import is_safe_url

from billing.models import BillingProfile, Card

STRIPE_PUBLIC_KEY = 'pk_test_ixXMDbREcjwgzM5oPghMBn0r00Q1kMltOU'

stripe.api_key = 'sk_test_EkmThKAelBXpI5emhMFE2fns00YtrrQBaZ'


def stripe_payment_view(request):
    billing_profile, billing_profile_created = BillingProfile.objects.get_or_create_billing_profile(request)

    if not billing_profile:
        return redirect('cart')

    # if request.user.is_authenticated():
    #     billing_profile = request.user.billing_profile
    #     my_customer_id = billing_profile.cutomer_id
    next_url = None
    next_ = request.GET.get('next')
    if next_url:
        next_url = next_

    context = {
        'public_key': STRIPE_PUBLIC_KEY,
        'next_url': next_url,

    }
    if request.method == 'POST':
        print(request.POST)
    return render(request, 'stripe_payment.html', context)


def create_payment(request):
    context = {
        'public_key': STRIPE_PUBLIC_KEY,

    }
    if request.method == 'POST' and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create_billing_profile(request)
        if not billing_profile:
            return HttpResponse({'message': 'Could Not Find This User'})

        token = request.POST.get('token')
        if token is not None:
            customer = stripe.Customer.retrieve(billing_profile.customer_id)
            card_response = customer.sources.create(source=token)
            new_card_object = Card.objects.add_new_card(billing_profile, card_response)
            print(new_card_object)
        return JsonResponse({'message': 'Success, Card Added Successfully'})
    return HttpResponse('Error', status=401)
