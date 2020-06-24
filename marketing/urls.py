from django.conf.urls import url

from marketing.views import MarketingPreferenceUpdateView

urlpatterns=[
    url('', MarketingPreferenceUpdateView.as_view(), name='marketing_email')
]