from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import UpdateView
from django.contrib.messages.views import SuccessMessageMixin

from .forms import MarketingPrefenceForm
from .models import MarketingPreference
from .utils import MailChimp
from .mixins import CsrfExemptMixin

MAILCHIMP_EMAIL_LIST_ID = getattr(settings, 'MAILCHIMP_EMAIL_LIST_ID', None)


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


class MailChimpWebHookView(CsrfExemptMixin, View):
    def post(self, request, *args, **kwargs):
        data = request.POST
        list_id = data.get('data[list_id]')
        if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
            email = data.get('data[email]')
            web_hook_type = data.get('type')
            response_status, response = MailChimp.change_subscription_status(email)
            subscription_status = response_status['status']

            is_subscribed = None
            is_mail_chimp_subscribed = None

            if subscription_status == 'subscribed':
                is_subscribed = True
                is_mail_chimp_subscribed = True

            elif subscription_status == 'unsubscribed':
                is_subscribed = False
                is_mail_chimp_subscribed = False

            if is_subscribed is not None and is_mail_chimp_subscribed is not None:
                qs = MarketingPreference.objects.filter(user__email__iexact=email)
                if qs.exists():
                    qs.update(subscribed=is_subscribed,
                              mail_chimp_subscribed=is_mail_chimp_subscribed,
                              is_mail_chimp_message=str(data))

        return HttpResponse('Thank You', status=200)


def mail_chimp_webhook_view(request):
    data = request.POST
    list_id = data.get('data[list_id]')
    if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
        email = data.get('data[email]')
        web_hook_type = data.get('type')
        response_status, response = MailChimp.change_subscription_status(email)
        subscription_status = response_status['status']

        is_subscribed = None
        is_mail_chimp_subscribed = None

        if subscription_status == 'subscribed':
            is_subscribed = True
            is_mail_chimp_subscribed = True

        elif subscription_status == 'unsubscribed':
            is_subscribed = False
            is_mail_chimp_subscribed = False

        if is_subscribed is not None and is_mail_chimp_subscribed is not None:
            qs = MarketingPreference.objects.filter(user__email__iexact=email)
            if qs.exists():
                qs.update(subscribed=is_subscribed,
                          mail_chimp_subscribed=is_mail_chimp_subscribed,
                          is_mail_chimp_message=str(data))

    return HttpResponse('Thank You', status=200)
