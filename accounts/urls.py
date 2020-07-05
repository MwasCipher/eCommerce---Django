from django.conf.urls import url
from django.views.generic import RedirectView

from .views import register_guest, RegisterView, LoginView, UserProfile

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^register/guest/$', register_guest, name='register_guest'),
    url(r'^$', UserProfile.as_view(), name='profile'),
    url(r'^accounts/', RedirectView.as_view(url='/account')),
    url(r'^settings/', RedirectView.as_view(url='/account')),
]
