from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import stripe

# Create your views here.
from django.utils.http import is_safe_url

STRIPE_PUBLIC_KEY = 'pk_test_ixXMDbREcjwgzM5oPghMBn0r00Q1kMltOU'

stripe.api_key = 'sk_test_EkmThKAelBXpI5emhMFE2fns00YtrrQBaZ'


def stripe_payment_view(request):

    next_ = request.GET.get('next')

    if is_safe_url(next_, request.get_host()):
        return redirect(next_)

    context = {
        'public_key': STRIPE_PUBLIC_KEY,

    }
    if request.method == 'POST':
        print(request.POST)
    return render(request, 'stripe_payment.html', context)


def create_payment(request):
    context = {
        'public_key': STRIPE_PUBLIC_KEY,

    }
    if request.method == 'POST' and request.is_ajax():
        print(request.POST)
        return JsonResponse({'message': 'Done'})
    return HttpResponse('Error', status=401)
