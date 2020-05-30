from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save

# Create your models here.
from accounts.models import GuestEmail
import stripe
User = settings.AUTH_USER_MODEL

stripe.api_key = 'sk_test_EkmThKAelBXpI5emhMFE2fns00YtrrQBaZ'


class BillingProfileManager(models.Manager):
    def get_or_create_billing_profile(self, request):
        user = request.user
        billing_profile_created = False
        billing_profile = None
        guest_email_id = request.session.get('guest_email_id')
        if user.is_authenticated():
            billing_profile, billing_profile_created = self.model.objects.get_or_create(user=user, email=user.email)
        elif guest_email_id is not None:
            guest_email_object = GuestEmail.objects.get(id=guest_email_id)
            billing_profile, billing_profile_created = self.model.objects.get_or_create(
                email=guest_email_object.email)
        else:
            pass

        return billing_profile, billing_profile_created


class BillingProfile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    customer_id = models.CharField(max_length=120, null=True, blank=True)

    objects = BillingProfileManager()

    def __str__(self):
        return self.email


def user_created_receiver(instance, created, sender, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)


post_save.connect(user_created_receiver, sender=User)
