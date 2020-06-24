from django import forms
from .models import MarketingPreference


class MarketingPrefenceForm(forms.ModelForm):
    subscribed = forms.BooleanField(label='Be Informed When New Products Are Available ', required=False)

    class Meta:
        model = MarketingPreference
        fields = [
            'subscribed'
        ]
