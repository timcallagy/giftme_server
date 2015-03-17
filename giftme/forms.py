from django import forms
from giftme.models import Gift

class GiftForm(forms.ModelForm):
    class Meta:
        model = Gift
        fields = ('owner_id','name','url','price',)

    def clean(self):
        print(self.cleaned_data)
        return self.cleaned_data
