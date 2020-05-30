from .models import Address
from django import forms


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'address_line_1',
            'address_line_2',
            'country',
            'state',
            'city',
            'postal_code',
        ]
