from django.conf.urls import url

from marketing.views import MarketingPreferenceUpdateView, MailChimpWebHookView

urlpatterns = [
    url('update_pref/', MarketingPreferenceUpdateView.as_view(), name='marketing_email'),
    url('webhook/', MailChimpWebHookView.as_view(), name='web_hook'),
]