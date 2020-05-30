from django.db import models
from billing.models import BillingProfile

# Create your models here.


ADDRESS_TYPES = (
    ('billing', 'Billing'),
    ('shipping', 'shipping'),
)


class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile)
    address_type = models.CharField(choices=ADDRESS_TYPES, max_length=120)
    address_line_1 = models.CharField(max_length=120)
    address_line_2 = models.CharField(max_length=120)
    country = models.CharField(max_length=120, default='Kenya')
    state = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    postal_code = models.CharField(max_length=120)

    def __str__(self):
        return str(self.billing_profile)

    def get_address(self):
        return '{line1}\n,{line2}\n,{country}-\n{state},\n{postal}\n,{city}\n'.format(
            line1=self.address_line_1 or '',
            line2=self.address_line_2 or '',
            country=self.country,
            city=self.city,
            state=self.state,
            postal=self.postal_code
        )
