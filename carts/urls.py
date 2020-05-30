from django.conf.urls import url

from .views import cart, cart_update, checkout, checkout_complete, cart_detail_api_view

urlpatterns = [
    url(r'^$', cart, name='cart'),
    url(r'^update/$', cart_update, name='update'),
    url(r'^checkout/$', checkout, name='checkout'),
    url(r'^checkout/success/$', checkout_complete, name='success'),
    url(r'^api/cart/$', cart_detail_api_view, name='api-cart'),
]
