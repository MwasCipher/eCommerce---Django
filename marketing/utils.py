from django.conf import settings
import requests
import json

MAILCHIMP_API_KEY = getattr(settings, 'MAILCHIMP_API_KEY', None)
MAILCHIMP_DATA_CENTER = getattr(settings, 'MAILCHIMP_DATA_CENTER', None)
MAILCHIMP_EMAIL_LIST_ID = getattr(settings, 'MAILCHIMP_EMAIL_LIST_ID', None)


class MailChimp(object):
    def __init__(self):
        super(MailChimp, self).__init__()
        self.key = MAILCHIMP_API_KEY
        self.api_url = "https://{dc}.api.mailchimp.com/3.0".format(dc=MAILCHIMP_DATA_CENTER)
        self.list_id = MAILCHIMP_EMAIL_LIST_ID
        self.list_endpoint = '{api_url}/lists/{list_id}'.format(api_url=self.api_url, list_id=self.list_id)

    def check_subscription_status(self, email):
        endpoint = self.api_url
        request_object = requests.get(endpoint, auth=('', self.key))
        return request_object.json()

    def check_valid_status(self, status):
        choices = ['subscribed', 'unsubscribed', 'pending', 'cleaned']
        if status not in choices:
            raise ValueError('Not A Valid Choice For Email Status')
        return status

    def add_email(self, email):
        status = 'subscribed'
        self.check_valid_status(status)
        data = {
            'email_address': email,
            'status': status
        }
        endpoint = self.list_endpoint + '/members'
        request_object = requests.post(endpoint, auth=('', self.key), data=json.dumps(data))
        return request_object.json()
