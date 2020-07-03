from django.conf.urls import url

from .views import register_guest, RegisterView, LoginView, UserProfile

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^register/guest/$', register_guest, name='register_guest'),
    url(r'^profile/$', UserProfile.as_view(), name='profile'),
]
