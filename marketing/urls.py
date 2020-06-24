from django.conf.urls import url

from marketing.views import MarketingPreferenceUpdateView

urlpatterns = [
    url('update_pref/', MarketingPreferenceUpdateView.as_view(), name='marketing_email'),
]