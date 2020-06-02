from django.conf.urls import url
from django.contrib.auth.urls import urlpatterns

from billing.views import stripe_payment_view, create_payment

urlpatterns = [
    url('stripe/', stripe_payment_view, name='stripe_payment'),
    url('stripe/create', create_payment, name='create_payment'),
]
