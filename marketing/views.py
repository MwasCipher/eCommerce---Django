from django.shortcuts import render
from django.views.generic import UpdateView

from .forms import MarketingPrefenceForm
from .models import MarketingPreference

# Create your views here.


class MarketingPreferenceUpdateView(UpdateView):
    form_class = MarketingPrefenceForm
    template_name = 'marketing_form.html'
    success_url = 'marketing_email'

    def get_context(self, **kwargs):
        context = super()

    def get_object(self):
        user = self.request.user
        marketing_preference_object, create_marketing_preference_object = MarketingPreference.objects.get_or_create(user=user)
        return marketing_preference_object


