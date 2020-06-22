from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save


# Create your models here.

class MarketingPreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    subscribed = models.BooleanField(default=True)
    mail_chimp_message = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


def marketing_pref_update_receiver(sender, instance, created, *args, **kwargs):
    if created:
        pass


post_save.connect(marketing_pref_update_receiver, sender=MarketingPreference)


def make_marketing_pref_receiver(instance, sender, created, *args, **kwargs):
    if created:
        MarketingPreference.objects.get_or_create(user=instance)


post_save.connect(make_marketing_pref_receiver, sender=settings.AUTH_USER_MODEL)
