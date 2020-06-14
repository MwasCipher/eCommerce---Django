from django.contrib import admin

# Register your models here.
from billing.models import BillingProfile, Card

admin.site.register(BillingProfile)
admin.site.register(Card)