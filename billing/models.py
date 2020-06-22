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


def billing_profile_created_receiver(instance, sender, *args, **kwargs):
    if not instance.customer_id and instance.email:
        customer = stripe.Customer.create(
            email=instance.email
        )
        instance.customer_id = customer.id
        print(customer)


pre_save.connect(billing_profile_created_receiver, sender=BillingProfile)


def user_created_receiver(instance, created, sender, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)


post_save.connect(user_created_receiver, sender=User)


class CardManager(models.Manager):
    def add_new_card(self, billing_profile, stripe_card_response):
        if str(stripe_card_response.object) == 'card':
            new_card = self.model(billing_profile=billing_profile,
                                  stripe_id=stripe_card_response.id,
                                  brand=stripe_card_response.brand,
                                  country=stripe_card_response.country,
                                  expiration_month=stripe_card_response.expiration_month,
                                  expiration_year=stripe_card_response.expiration_year,
                                  last_four_digits=stripe_card_response.last_four_digits)

            new_card.save()
            return new_card

        return None


class Card(models.Model):
    billing_profile = models.ForeignKey(BillingProfile)
    stripe_id = models.CharField(max_length=120, null=True, blank=True)
    brand = models.CharField(max_length=120, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    expiration_month = models.IntegerField()
    expiration_year = models.IntegerField()
    last_four_digits = models.CharField(max_length=4, null=True, blank=True)
    default = models.BooleanField(default=True)

    objects = CardManager()

    def __str__(self):
        return "{} {}".format(self.brand, self.last_four_digits)


class ChargeManager(models.Manager):
    def charge_customer(self, billing_profile, order_object, card=None):
        card_object = card
        if card_object is None:
            cards = billing_profile.card_set.filter(default=True)
            if cards.exists():
                card_object = cards.first()

        if card is None:
            return False, 'No Cards Available'
        charge = stripe.Charge.create(amount=int(order_object.total*100),
                                      currency='usd',
                                      customer=billing_profile.stripe_id,
                                      source=card_object.stripe_id,
                                      description='Charge For Cheech')

        new_charge_object = self.model(
            billing_profile=billing_profile,
            stripe_id=charge.id,
            paid=charge.paid,
            refund=charge.refund,
            outcome=charge.outcome,
            outcome_type=charge.outcome['type'],
            seller_message=charge.outcome.get('seller_message'),
            risk_level=charge.outcome.get('risk_level'),

        )
        return


class Charge(models.Model):
    billing_profile = models.ForeignKey(BillingProfile)
    stripe_id = models.CharField(max_length=120, null=True, blank=True)
    paid = models.BooleanField(default=False)
    refund = models.BooleanField(default=False)
    outcome = models.TextField(blank=True, null=True)
    outcome_type = models.CharField(max_length=120, null=True, blank=True)
    seller_message = models.CharField(max_length=120, null=True, blank=True)
    risk_level = models.CharField(max_length=120, null=True, blank=True)
