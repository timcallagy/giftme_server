from django import forms
from django.contrib import admin

from giftme.models import Gift


class GiftAdmin(forms.ModelForm):
    class Meta:
        model = Gift

admin.site.register(Gift)
