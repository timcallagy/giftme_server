from django import forms
from giftme.models import UserProfile, Gift

class GiftForm(forms.ModelForm):
    class Meta:
        model = Gift
        fields = ('owner','name','url','price',)

    def clean(self):
        return self.cleaned_data
