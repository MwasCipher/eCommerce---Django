from django.shortcuts import render
import stripe

# Create your views here.
STRIPE_PUBLIC_KEY = ''
stripe.api_key = 'sk_test_EkmThKAelBXpI5emhMFE2fns00YtrrQBaZ'


def stripe_payment_view(request):
    context = {
        'public_key': STRIPE_PUBLIC_KEY,

    }
    if request.method == 'POST':
        print(request.POST)
    return render(request, 'stripe_payment.html', context)
