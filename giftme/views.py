import stripe
import urllib2
import requests
import json
import pytz
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from giftme.forms import GiftForm
from giftme.models import Gift, Contribution, FacebookSession
from django.template import RequestContext
from django.http import HttpResponse
from django.middleware.csrf import _get_new_csrf_key as get_new_csrf_key
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder

@csrf_exempt
def login(request):
    if request.method == 'POST':
        accessToken = request.POST['accessToken']
        expiresIn = int(request.POST['expiresIn'])
        userID = request.POST['userID']
        url = 'https://graph.facebook.com/v2.0/me?access_token=' + accessToken + '&method=get&pretty=0&sdk=joey'
        response = (requests.get(url)).json()
        id = response.get('id') 
        if (id == userID):
            expiryTime = datetime.now().replace(tzinfo=pytz.utc) + timedelta(seconds=expiresIn)
            try:
                session = FacebookSession.objects.get(userID=id)
                session.accessToken = accessToken
                session.expiryTime = expiryTime
            except FacebookSession.DoesNotExist:
                name = urllib2.unquote((response.get('name')).encode('ascii'))
                session = FacebookSession(userID=userID, name=name, accessToken=accessToken, expiryTime=expiryTime)
            session.save()
            return HttpResponse('true')
        else:
            return HttpResponse('false')

def wakeup(request):
    return HttpResponse('Success')

def get_csrf_token(request):
    csrftoken = get_new_csrf_key()
    return HttpResponse(csrftoken)

@csrf_exempt
def add_gift(request):
    """
    if request.method == 'POST':
        accessToken=request.POST['accessToken']
        userID=request.POST['userID']
        try:
            facebookSession = FacebookSession.objects.get(userID=userID)
            if facebookSession.accessToken==accessToken and facebookSession.expiryTime > datetime.utcnow().replace(tzinfo=pytz.utc):
                add_gift_form = GiftForm(data=request.POST)
                if add_gift_form.is_valid():
                    gift = add_gift_form.save(commit=False)
                    if not gift.url.startswith("http"):
                        gift.url = "http://" + gift.url
                    try:
                        urlopen_res = urllib2.urlopen(gift.url)
                    except:
                        return HttpResponse('Invalid URL')
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
                    return HttpResponse('Invalid amount')
            else:
                return HttpResponse('Error - not authorized')
        except FacebookSession.DoesNotExist:
            return HttpResponse('Error - not authenticated')
    else:
        return HttpResponse('false')
    """
    context = RequestContext(request)
        add_gift_form = GiftForm(data=request.POST)
        if add_gift_form.is_valid():
            gift = add_gift_form.save(commit=False)
            if not gift.url.startswith("http"):
                gift.url = "http://" + gift.url
            urlopen_res = urllib2.urlopen(gift.url)
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
    gifts = Gift.objects.filter(owner_id = id ).order_by('-crowdfunded');
    data = serializers.serialize('json', gifts)
    return HttpResponse(data)

def get_gift(request, pk):
    try:
        gift = Gift.objects.get(pk = pk );
    except Gift.DoesNotExist:
        return HttpResponse('Gift does not exist')
    data = serializers.serialize('json', [gift])
    return HttpResponse(data)

def get_friends_gifts(request, id):
    gifts = Gift.objects.filter(owner_id = id).order_by('-crowdfunded');
    data = serializers.serialize('json', gifts)
    return HttpResponse(data)

@csrf_exempt
def delete_gift(request, pk):
    """ This code does authorization check
    accessToken=request.POST['accessToken']
    userID=request.POST['userID']
    try:
        facebookSession = FacebookSession.objects.get(userID=userID)
        if facebookSession.accessToken==accessToken and facebookSession.expiryTime > datetime.utcnow().replace(tzinfo=pytz.utc):
            Gift.objects.get(pk=pk).delete()
            return HttpResponse('true')
        else:
            return HttpResponse('false')
    except FacebookSession.DoesNotExist:
        return HttpResponse('false')
    """
    Gift.objects.get(pk=pk).delete()
    return HttpResponse('true')



@csrf_exempt
def pay(request, pk):
    """ This code does authorization check
    if request.method == 'POST':
        try:
            contributor_id = request.POST['contributor_id']
            facebookSession = FacebookSession.objects.get(userID=contributor_id)
            accessToken = request.POST['accessToken']
            if facebookSession.accessToken==accessToken and facebookSession.expiryTime > datetime.utcnow().replace(tzinfo=pytz.utc):
                stripe.api_key = settings.STRIPE_SECRET
                token = request.POST['token']
                amount = float(request.POST['amount'])
                contributor_name = urllib2.unquote((request.POST['contributor_name']).encode('ascii'))
                message = request.POST.get('message', '')
                timestamp = datetime.fromtimestamp(float(request.POST['timestamp'])/1000)
                try:
                    charge = stripe.Charge.create(
                            amount=int(amount*100),
                            currency="usd",
                            card=token,
                            description="GiftMe payment"
                            )
                except stripe.CardError, ce:
                    return HttpResponse(ce)
                try:
                    gift = Gift.objects.get(pk=pk)
                    gift.crowdfunded += amount
                    gift.save()
                except Gift.DoesNotExist:
                    return HttpResponse('Error - Gift does not exist')
                contributed_to = gift.owner_id
                contribution = Contribution(gift=gift, gift_name= gift.name, contributor_id=contributor_id, contributor_name=contributor_name, contributed_to=contributed_to, amount=amount, message=message, contribution_date=timestamp, stripe_charge=charge.id)
                contribution.save()
                data = serializers.serialize('json', [contribution])
                return HttpResponse(data)
            else:
                return HttpResponse('Error - not authorized')
        except FacebookSession.DoesNotExist:
            return HttpResponse('Error - not authenticated')
    else:
        return HttpResponse('Error - This should be a POST request')
    """
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET
        token = request.POST['token']
        amount = float(request.POST['amount'])
        contributor_id = request.POST['contributor_id']
        contributor_name = urllib2.unquote((request.POST['contributor_name']).encode('ascii'))
        message = request.POST.get('message', '')
        timestamp = datetime.fromtimestamp(float(request.POST['timestamp'])/1000)
        accessToken = request.POST['accessToken']
        try:
            charge = stripe.Charge.create(
                    amount=int(amount*100),
                    currency="usd",
                    card=token,
                    description="GiftMe payment"
                    )
        except stripe.CardError, ce:
            return HttpResponse(ce)
        try:
            gift = Gift.objects.get(pk=pk)
            gift.crowdfunded += amount
            gift.save()
        except Gift.DoesNotExist:
            return HttpResponse('Error - Gift does not exist')
        contributed_to = gift.owner_id
        contribution = Contribution(gift=gift, gift_name= gift.name, contributor_id=contributor_id, contributor_name=contributor_name, contributed_to=contributed_to, amount=amount, message=message, contribution_date=timestamp, stripe_charge=charge.id)
        contribution.save()
        data = serializers.serialize('json', [contribution])
        return HttpResponse(data)
    else:
        return HttpResponse('Error - This should be a POST request')

def get_contributions(request, pk):
    contributions = Contribution.objects.filter(gift = pk );
    data = serializers.serialize('json', contributions)
    return HttpResponse(data)
