from django import forms
from django.contrib import admin
from giftme.models import Gift, Contribution, FacebookSession

class GiftAdmin(forms.ModelForm):
    class Meta:
        model = Gift

class ContributionAdmin(forms.ModelForm):
    class Meta:
        model = Contribution

class FacebookSessionAdmin(forms.ModelForm):
    class Meta:
        model = FacebookSession

admin.site.register(Gift)
admin.site.register(Contribution)
admin.site.register(FacebookSession)
