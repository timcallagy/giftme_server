import stripe
import urllib2
import requests
import json
import pytz
import logging
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
from giftme.forms import GiftForm
from giftme.models import Gift, Contribution, FacebookSession
from django.template import RequestContext
from django.http import HttpResponse
from django.middleware.csrf import _get_new_csrf_key as get_new_csrf_key
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string


@csrf_exempt
def login(request):
    if request.method == 'POST':
        accessToken = request.POST['accessToken']
        expiresIn = int(request.POST['expiresIn'])
        userID = request.POST['userID']
        url = 'https://graph.facebook.com/v2.0/me?access_token=' + accessToken + '&method=get&pretty=0&sdk=joey'
        response = (requests.get(url)).json()
        print(response)
        id = response.get('id') 
        if (id == userID):
            expiryTime = datetime.now().replace(tzinfo=pytz.utc) + timedelta(seconds=expiresIn)
            try:
                session = FacebookSession.objects.get(userID=id)
                session.accessToken = accessToken
                session.expiryTime = expiryTime
            except FacebookSession.DoesNotExist:
                name = response.get('name').encode('utf-8')
                email = response.get('email', '').encode('utf-8')
                gender = response.get('gender', '').encode('utf-8')
                joined_date = datetime.utcnow().replace(tzinfo=pytz.utc)
                session = FacebookSession(userID=userID, name=name, accessToken=accessToken, expiryTime=expiryTime, email=email, joined_date=joined_date)
            session.save()
            return HttpResponse('true')
        else:
            return HttpResponse('false')

@csrf_exempt
def wakeup(request):
    supportedVersions = ['0.0.21']
    logger = logging.getLogger('giftme')
    logger.debug('In wakeup function.')
    if request.method == 'POST':
        clientVersion = request.POST['clientVersion']
        logger.debug('Client version: ' + str(clientVersion) + '.')
        if clientVersion in supportedVersions:
            logger.debug('Supported client version: ' + str(clientVersion) + '.')
            return HttpResponse('Success')
        else:
            logger.debug('Unsupported client version: ' + str(clientVersion) + '.')
            data = json.dumps({'message': 'Unsupported client version. Update at:', 'url': 'https://play.google.com/store/apps/details?id=co.giftmeapp.gift_me'})
            return HttpResponse(data) 
    else:
        return HttpResponse('Error')

def get_csrf_token(request):
    csrftoken = get_new_csrf_key()
    return HttpResponse(csrftoken)

@csrf_exempt
def add_gift(request):
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
                    timestamp = datetime.utcnow().replace(tzinfo=pytz.utc)
                    gift.added_date = timestamp
                    gift.owner_name = urllib2.unquote((request.POST['userName']).encode('ascii'))
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


@csrf_exempt
def pay(request, pk):
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
                contributed_to_name = urllib2.unquote((request.POST['contributed_to_name']).encode('ascii'))
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
                contribution = Contribution(gift=gift, gift_name= gift.name, gift_pic= gift.pic, contributor_id=contributor_id, contributor_name=contributor_name, contributed_to=contributed_to, contributed_to_name=contributed_to_name, amount=amount, message=message, contribution_date=timestamp, stripe_charge=charge.id)
                contribution.save()
                # Send notification email to gift receiver
                receiver_session = FacebookSession.objects.get(userID=contributed_to)
                if receiver_session.email:
                    send_giftme_email(receiver_session.email, 'You have received a gift contribution!', 'gift_contribution', {'contributor_name': contributor_name, 'gift_name': gift.name, 'gift_amount': amount, 'message': message }, facebookSession.receiveEmails)
                data = serializers.serialize('json', [contribution])
                return HttpResponse(data)
            else:
                return HttpResponse('Error - not authorized')
        except FacebookSession.DoesNotExist:
            return HttpResponse('Error - not authenticated')
    else:
        return HttpResponse('Error - This should be a POST request')

def get_contributions(request, pk):
    contributions = Contribution.objects.filter(gift = pk );
    data = serializers.serialize('json', contributions)
    return HttpResponse(data)


@csrf_exempt
def user_settings(request, id):
    if request.method == 'POST':
        accessToken=request.POST['accessToken']
        userID=request.POST['userID']
        try:
            facebookSession = FacebookSession.objects.get(userID=userID)
            if facebookSession.accessToken==accessToken and facebookSession.expiryTime > datetime.utcnow().replace(tzinfo=pytz.utc):
                receiveEmails = request.POST['receiveEmails']
                if receiveEmails == 'true':
                    facebookSession.receiveEmails=True
                else:
                    facebookSession.receiveEmails=False
                birthday_day=request.POST['birthday_day']
                birthday_month=request.POST['birthday_month']
                facebookSession.birthday=date(1900, int(birthday_month), int(birthday_day))
                facebookSession.save()
                data = serializers.serialize('json', {facebookSession})
                return HttpResponse(data)
            else:
                return HttpResponse('Error - not authorized')
        except FacebookSession.DoesNotExist:
            return HttpResponse('Error - not authenticated')
    elif request.method == 'GET':
        my_settings = FacebookSession.objects.filter(userID = id)
        data = serializers.serialize('json', my_settings)
        return HttpResponse(data)


@csrf_exempt
def get_notifications(request, id):
    accessToken=request.POST['accessToken']
    url = 'https://graph.facebook.com/v2.0/me/friends?access_token=' + accessToken + '&method=get&pretty=0&sdk=joey'
    response = (requests.get(url)).json()
    data = response.get('data')
    friendIDs = []
    for f in data:
        friendIDs.append(f.get('id'))
    
    gifts = Gift.objects.filter(owner_id__in = friendIDs).order_by('-added_date')[:4]

    now = (datetime.now().replace(year=1900))
    now_plus_1_month = now + timedelta(days=30)
    birthdays = FacebookSession.objects.filter(birthday__gt = now, birthday__lt = now_plus_1_month)
    
    # Also add this user's id to the list, so that his/her contributions are also found.
    friendIDs.append(id)

    contributions_to = Contribution.objects.filter(contributed_to__in = friendIDs).order_by('-contribution_date')[:4]
    for c in contributions_to:
        if c.contributed_to == id:
            c.contributed_to_name = 'You'

    contributions_from = Contribution.objects.filter(contributor_id__in = friendIDs).order_by('-contribution_date')[:4]
    for c in contributions_from:
        if c.contributor_id == id:
            c.contributor_name = 'You'

    time_period_week = datetime.now() - timedelta(days=7)
    recent_friends = FacebookSession.objects.filter(userID__in = friendIDs, joined_date__gt=time_period_week).order_by('-joined_date')[:3]
    birthdays = serializers.serialize('json', birthdays)
    gifts = serializers.serialize('json', gifts)
    contributions_to = serializers.serialize('json', contributions_to)
    contributions_from = serializers.serialize('json', contributions_from)
    recent_friends = serializers.serialize('json', recent_friends)
    combined_data = {'contributions_to': contributions_to, 'contributions_from': contributions_from, 'recent_friends': recent_friends, 'gifts': gifts, 'birthdays': birthdays}
    return HttpResponse(json.dumps(combined_data))



################################
###
### Functions
###
################################


# Handles email notification sending.
def send_giftme_email(to, subject, content_name, variables, email_notifications_requested):
    if to and email_notifications_requested == True:
        from_email = 'GiftMe@giftme.com'
        text_content = render_to_string('giftme/emails/' + content_name + '.txt', variables)
        html_content = render_to_string('giftme/emails/' + content_name + '.html', variables)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        #msg.mixed_subtype = 'related'
        #image = open(settings.STATIC_PATH + '/img/logo.png', 'rb')
        #msg_img = MIMEImage(image.read())
        #image.close()
        #msg_img.add_header('Content-ID', 'logo.png')
        #msg_img.add_header('From', 'Yanga')
        #msg.attach(msg_img)
        msg.send()
    return
