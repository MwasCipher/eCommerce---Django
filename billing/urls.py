from django.conf.urls import url
from django.contrib.auth.urls import urlpatterns

from billing.views import stripe_payment_view

urlpatterns = [
    url('stripe/', stripe_payment_view, name='stripe_payment')
]
