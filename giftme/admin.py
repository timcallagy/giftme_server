from django import forms
from django.contrib import admin

from giftme.models import Gift, Contribution

class GiftAdmin(forms.ModelForm):
    class Meta:
        model = Gift

class ContributionAdmin(forms.ModelForm):
    class Meta:
        model = Contribution

admin.site.register(Gift)
admin.site.register(Contribution)
