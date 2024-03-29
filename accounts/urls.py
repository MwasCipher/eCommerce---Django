from django.conf.urls import url
from django.views.generic import RedirectView

from products.views import UserProductHistoryView
from .views import GuestRegisterView, RegisterView, LoginView, UserProfile, AccountEmailActivationView, \
    UserDetailsUpdateView

urlpatterns = [
    url(r'^$', UserProfile.as_view(), name='accounts'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^details/$', UserDetailsUpdateView.as_view(), name='update-user-details'),
    url(r'^register/guest/$', GuestRegisterView.as_view(), name='register_guest'),
    url(r'^products/history/$', UserProductHistoryView.as_view(), name='products-history'),
    url(r'^$', UserProfile.as_view(), name='profile'),
    url(r'^accounts/', RedirectView.as_view(url='account')),
    url(r'^settings/', RedirectView.as_view(url='/account')),
    url(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/',
        AccountEmailActivationView.as_view(), name='email-activate'),
    url(r'^email/resend-activation/',
        AccountEmailActivationView.as_view(), name='resend-activation'),
]
