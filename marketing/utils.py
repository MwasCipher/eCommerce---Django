from django.conf import settings
import requests
import json
import hashlib
import re

MAILCHIMP_API_KEY = getattr(settings, 'MAILCHIMP_API_KEY', None)
MAILCHIMP_DATA_CENTER = getattr(settings, 'MAILCHIMP_DATA_CENTER', None)
MAILCHIMP_EMAIL_LIST_ID = getattr(settings, 'MAILCHIMP_EMAIL_LIST_ID', None)


def check_email(email):
    if not re.match(r'.+@.+\..+', email):
        raise ValueError('String Passed is Not A Valid Email Address')
    return email


def get_subscriber_hash(member_email):
    check_email(member_email)
    member_email = member_email.lower().encode()
    m = hashlib.md5(member_email)
    return m.hexdigest()


def get_members_endpoint(self):
    return self.list_endpoint + '/members/'


class MailChimp(object):
    def __init__(self):
        super(MailChimp, self).__init__()
        self.key = MAILCHIMP_API_KEY
        self.api_url = "https://{dc}.api.mailchimp.com/3.0".format(dc=MAILCHIMP_DATA_CENTER)
        self.list_id = MAILCHIMP_EMAIL_LIST_ID
        self.list_endpoint = '{api_url}/lists/{list_id}'.format(api_url=self.api_url, list_id=self.list_id)

    def change_subscription_status(self, email, status='unsubscribed'):
        hashed_email = get_subscriber_hash(email)
        data = {
            'status': self.check_valid_status(status)
        }
        endpoint = self.get_members_endpoint() + hashed_email
        request_object = requests.put(endpoint, data=json.dumps(data), auth=('', self.key))
        return request_object.json()

    def check_subscription_status(self, email):
        hashed_email = get_subscriber_hash(email)
        endpoint = self.get_members_endpoint() + hashed_email
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
        endpoint = self.get_members_endpoint()
        request_object = requests.post(endpoint, auth=('', self.key), data=json.dumps(data))
        return request_object.json()
