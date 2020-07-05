from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^password/change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    url(r'^password/change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    url(r'^password/reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    url(r'^password/reset/done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),


]
