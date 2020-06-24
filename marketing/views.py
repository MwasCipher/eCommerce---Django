from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import UpdateView

from .forms import MarketingPrefenceForm
from .models import MarketingPreference

# Create your views here.


class MarketingPreferenceUpdateView(UpdateView):
    form_class = MarketingPrefenceForm
    template_name = 'marketing_form.html'
    success_url = 'update_pref'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated():
            return HttpResponse('Not Allowed', status=400)

        return super(MarketingPreferenceUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(MarketingPreferenceUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Email Preferences'

    def get_object(self):
        user = self.request.user
        marketing_preference_object, create_marketing_preference_object = MarketingPreference.objects.get_or_create(
                                                                                                           user=user)
        return marketing_preference_object


