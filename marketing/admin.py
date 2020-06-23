from django.contrib import admin

# Register your models here.
from marketing.models import MarketingPreference


class MarketingPreferenceAdmin(admin.ModelAdmin):
    readonly_fields = ['mail_chimp_message', 'mail_chimp_subscribed', 'timestamp', 'updated']
    list_display = ['__str__', 'mail_chimp_subscribed', 'updated']

    class Meta:
        model = MarketingPreference
        fields = ['user', 'subscribed', 'mail_chimp_message']


admin.site.register(MarketingPreference, MarketingPreferenceAdmin)
