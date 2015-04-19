from django import forms
from giftme.models import Gift

class GiftForm(forms.ModelForm):
    class Meta:
        model = Gift
        fields = ('owner_id','name','url','price', 'description',)

    def clean(self):
        return self.cleaned_data
