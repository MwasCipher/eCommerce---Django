from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from django.contrib.messages.views import SuccessMessageMixin

from .forms import MarketingPrefenceForm
from .models import MarketingPreference

# Create your views here.


class MarketingPreferenceUpdateView(UpdateView, SuccessMessageMixin):
    form_class = MarketingPrefenceForm
    template_name = 'marketing_form.html'
    success_url = 'update_pref'
    success_message = 'Your Email Preferences Updated Successfully'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated():
            return redirect('login?next=update_pref')

        return super(MarketingPreferenceUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(MarketingPreferenceUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Email Preferences'

    def get_object(self):
        user = self.request.user
        marketing_preference_object, create_marketing_preference_object = MarketingPreference.objects.get_or_create(
                                                                                                           user=user)
        return marketing_preference_object


