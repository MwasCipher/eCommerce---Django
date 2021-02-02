from django.conf.urls import url
from django.views.generic import RedirectView

from .views import register_guest, RegisterView, LoginView, UserProfile, AccountEmailActivationView

urlpatterns = [
    url(r'^$', UserProfile.as_view(), name='accounts'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^register/guest/$', register_guest, name='register_guest'),
    url(r'^$', UserProfile.as_view(), name='profile'),
    url(r'^accounts/', RedirectView.as_view(url='account')),
    url(r'^settings/', RedirectView.as_view(url='/account')),
    url(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/',
        AccountEmailActivationView.as_view(), name='email-activate'),
    url(r'^email/resend-activation/',
        AccountEmailActivationView.as_view(), name='resend-activation'),
]
