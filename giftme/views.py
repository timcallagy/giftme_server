from giftme.forms import GiftForm
from giftme.models import Gift
from django.template import RequestContext
from django.http import HttpResponse
from django.middleware.csrf import _get_new_csrf_key as get_new_csrf_key
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.conf import settings
import json
from django.core.serializers.json import DjangoJSONEncoder

from urllib2 import urlopen
from bs4 import BeautifulSoup
#import urllib

import stripe

def get_csrf_token(request):
    csrftoken = get_new_csrf_key()
    return HttpResponse(csrftoken)

@csrf_exempt
def add_gift(request):
    context = RequestContext(request)
    if request.method == 'POST':
        add_gift_form = GiftForm(data=request.POST)
        if add_gift_form.is_valid():
            gift = add_gift_form.save(commit=False)
            if not gift.url.startswith("http"):
                gift.url = "http://" + gift.url
            urlopen_res = urlopen(gift.url)
            html = urlopen_res.read()
            soup = BeautifulSoup(html)
            try:
                img = soup.find('img', {'id': 'imgBlkFront'}) or soup.find('img', {'id': 'landingImage'}) or soup.find('img', {'id': 'detailImg'})
                pic_url = img['src']
            except TypeError:
                pic_url = "img/generic_gift.png"
            gift.pic = pic_url
            gift.save()
            return HttpResponse('true')
        else:
            return HttpResponse('false')
    else:
        return HttpResponse('false')

def get_gifts(request, id):
    gifts = Gift.objects.filter(owner_id = id );
    data = serializers.serialize('json', gifts)
    return HttpResponse(data)

def get_friends_gifts(request, id):
    gifts = Gift.objects.filter(owner_id = id);
    data = serializers.serialize('json', gifts)
    return HttpResponse(data)

@csrf_exempt
def delete_gift(request, pk):
    Gift.objects.get(pk=pk).delete()
    return HttpResponse()

@csrf_exempt
def pay(request, pk):
    stripe.api_key = settings.STRIPE_SECRET
    token = request.POST['token']
    amount = float(request.POST['amount'])
    try:
        charge = stripe.Charge.create(
                amount=int(amount*100),
                currency="usd",
                card=token,
                description="GiftMe payment"
                )
        gift = Gift.objects.get(pk=pk)
        gift.crowdfunded += amount
        gift.save()
        return HttpResponse('true')
    except stripe.CardError, ce:
        print("Payment failed")
        print(ce)
        return HttpResponse(ce)
