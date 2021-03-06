import stripe
import urllib2
import requests
import json
import pytz
import logging
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
from email.MIMEImage import MIMEImage
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
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.shortcuts import redirect
from numpy import asarray


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
    supportedVersions = ['0.0.25']
    logger = logging.getLogger('giftme')
    logger.debug('In wakeup function.')
    print('in wakeup')
    if request.method == 'POST':
        clientVersion = request.POST['clientVersion']
        print(clientVersion)
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
                    if "www.amazon." not in gift.url:
                        return HttpResponse('Not Amazon')
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
                    #gift.owner_name = urllib2.unquote((request.POST['userName']).encode('ascii'))
                    gift.owner_name = facebookSession.name
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
        gift = Gift.objects.get(pk = pk )
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
                contributor_name = facebookSession.name
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
                contributed_to_name = gift.owner_name
                print('Contributed to:')
                print(contributed_to_name)
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


@csrf_exempt
def pay_new(request, pk):
    if request.method == 'POST':
        try:
            contributor_id = request.POST['contributor_id']
            facebookSession = FacebookSession.objects.get(userID=contributor_id)
            accessToken = request.POST['accessToken']
            if facebookSession.accessToken==accessToken and facebookSession.expiryTime > datetime.utcnow().replace(tzinfo=pytz.utc):
                token = request.POST['token']
                amount = int(request.POST['amount'])
                contributor_name = facebookSession.name
                message = request.POST.get('message', '')
                timestamp = datetime.fromtimestamp(float(request.POST['timestamp'])/1000)
                payments_provider = request.POST['provider']
                if payments_provider == "stripe":
                    stripe.api_key = settings.STRIPE_SECRET
                    try:
                        charge = stripe.Charge.create(
                                amount=int(amount*100),
                                currency="usd",
                                card=token,
                                description="GiftMe payment"
                                )
                        payment_id = charge.id
                    except stripe.CardError, ce:
                        return HttpResponse(ce)
                elif payments_provider == "paypal":
                    payment_id = token

                try:
                    gift = Gift.objects.get(pk=pk)
                    gift.crowdfunded += amount
                    gift.save()
                except Gift.DoesNotExist:
                    return HttpResponse('Error - Gift does not exist')
                contributed_to = gift.owner_id
                contributed_to_name = gift.owner_name

                ### Change name of "stripe_charge" below! ###

                contribution = Contribution(gift=gift, gift_name= gift.name, gift_pic= gift.pic, contributor_id=contributor_id, contributor_name=contributor_name, contributed_to=contributed_to, contributed_to_name=contributed_to_name, amount=amount, message=message, contribution_date=timestamp, stripe_charge=payment_id)
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
    gift = Gift.objects.filter(pk = pk).values('id', 'owner_id', 'owner_name', 'name', 'price', 'crowdfunded', 'pic')
    gift = list(gift)
    contributions_to = Contribution.objects.filter(gift_id = pk).values('contributor_id', 'contributor_name', 'gift', 'gift_name', 'amount').order_by('-contribution_date')
    contributions_to = list(contributions_to)
    gift = json.dumps(gift)
    contributions_to = json.dumps(contributions_to)
    combined_data = {'contributions_to': contributions_to, 'gift': gift}
    return HttpResponse(json.dumps(combined_data))


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
    
    gifts = Gift.objects.filter(owner_id__in = friendIDs).values('id', 'owner_id', 'owner_name', 'name', 'pic').order_by('-added_date')[:4]
    gifts = list(gifts)

    now = (datetime.now().replace(year=1900))
    now_plus_1_month = now + timedelta(days=30)
    birthdays = FacebookSession.objects.filter(userID__in = friendIDs, birthday__gt = now, birthday__lt = now_plus_1_month).values('userID','name', 'birthday')
    for b in birthdays:
        b['birthday'] = b['birthday'].strftime("%B %d")
    birthdays = list(birthdays)
    
    time_period_week = datetime.now() - timedelta(days=7)
    recent_friends = FacebookSession.objects.filter(userID__in = friendIDs, joined_date__gt=time_period_week).values('userID', 'name').order_by('-joined_date')[:3]
    recent_friends = list(recent_friends)
    
    # Also add this user's id to the list, so that his/her contributions are also found.
    friendIDs.append(id)

    contributions_to = Contribution.objects.filter(contributed_to__in = friendIDs).values('contributed_to', 'contributed_to_name', 'gift', 'gift_name', 'amount').order_by('-contribution_date')[:2]
    contributions_to = list(contributions_to)
    for c in contributions_to:
        if c['contributed_to'] == id:
            c['contributed_to_name'] = 'You'

    contributions_from = Contribution.objects.filter(contributor_id__in = friendIDs).values('contributor_id', 'contributor_name', 'gift', 'gift_name', 'amount').order_by('-contribution_date')[:2]
    contributions_from = list(contributions_from)
    for c in contributions_from:
        if c['contributor_id'] == id:
            c['contributor_name'] = 'You'

    birthdays = json.dumps(birthdays)
    gifts = json.dumps(gifts)
    contributions_to = json.dumps(contributions_to)
    contributions_from = json.dumps(contributions_from)
    recent_friends = json.dumps(recent_friends)
    combined_data = {'contributions_to': contributions_to, 'contributions_from': contributions_from, 'recent_friends': recent_friends, 'gifts': gifts, 'birthdays': birthdays}
    return HttpResponse(json.dumps(combined_data))


def web(request):
    context = RequestContext(request)
    return render_to_response('giftme/index.html', {}, context) 


def web_gift_list(request, id):
    """
    Function to get gift list and return for display along with form with selection of appropriate amounts.

    Parameters
    ------------
    id: int
        Facebook userid which is the owner_id of the gift.
    """
    gifts = Gift.objects.filter(owner_id = id).order_by('-crowdfunded');
    for gift in gifts:
        gift.formatPricesUSD()
        gift.formatPricesEUR(usd_to_eur_rate())
        gift.add_valid_amountsUSD()
        gift.add_valid_amountsEUR(usd_to_eur_rate())
        gift.priceEUR = gift.price*usd_to_eur_rate()
    session = FacebookSession.objects.get(userID=id)
    context = {'gifts_list': gifts, 'owner_id': id, 'owner_name': session.name}
    return render(request, 'giftme/gift_list.html', context) 


def web_gift(request, gift_id):
    """
    Function to get specified gift and return for display along with form with selection of appropriate amounts.

    Parameters
    ------------
    gift_id: int
        Identifier of gift. 
    """
    gift = Gift.objects.get(id = gift_id)
    gift.formatPricesUSD()
    gift.formatPricesEUR(usd_to_eur_rate())
    gift.add_valid_amountsUSD()
    gift.add_valid_amountsEUR(usd_to_eur_rate())
    gift.priceEUR = gift.price*usd_to_eur_rate()
    context = {'gifts_list': [gift], 'owner_id': gift.owner_id, 'owner_name': gift.owner_name}
    return render(request, 'giftme/gift_list.html', context) 


def web_pay(request, id):
    """
    Function to process the form containg the amount field and render template which will display payment form with stripe payment button.

    Parameters
    -----------
    id: int
        The id of the gift to display details and form for.
    """
    gift = Gift.objects.get(pk=id)
    gift.formatPricesUSD()
    gift.formatPricesEUR(usd_to_eur_rate())
    gift.remaining = float(gift.price - gift.crowdfunded)

    if request.method == 'POST':
        contributionAmount = float(request.POST["contributionAmount"])
        currency = request.POST["currency"]
        rate = usd_to_eur_rate()
        if currency == "USD":
            contributionAmountUSD = contributionAmount
            contributionAmountEUR = contributionAmount*rate
        else: 
            contributionAmountUSD = contributionAmount/rate
            contributionAmountEUR = contributionAmount
        context = {'gift': gift, 'amountUSD': contributionAmountUSD * 100, 'displayAmountUSD': "{0:.2f}".format(contributionAmountUSD), 'amountEUR': contributionAmountEUR * 100, 'displayAmountEUR': "{0:.2f}".format(contributionAmountEUR), 'currency': currency} # multiply by 100 since stripe takes cents

    return render(request, 'giftme/pay.html', context) 


def web_pay_process(request, id):
    gift = Gift.objects.get(pk=id)
    gift.formatPricesUSD()
    gift.formatPricesEUR(usd_to_eur_rate())

    if request.method == 'POST':
        stripeToken = request.POST["stripeToken"]
        amount = float(request.POST['contributedAmount'])
        currency = request.POST['currency'] 
        print(int(amount*100))
        stripe.api_key = settings.STRIPE_SECRET
        # The actual card charge happens here
        try:
            charge = stripe.Charge.create(
                    amount=int(amount*100),
                    currency=currency,
                    card=stripeToken,
                    description="GiftMe payment"
                    )
            payment_id = charge.id
        except stripe.CardError, ce:
            return HttpResponse(ce)
        contributor_id = 0
        contributor_name = request.POST["contributorName"]
        if contributor_name == '':
            contributor_name = 'Someone'
        contributed_to = gift.owner_id
        contributed_to_name = gift.owner_name
        message = request.POST['personalMessage'] 
        timestamp = datetime.now()
        if currency == "EUR":
            amount = amount/usd_to_eur_rate()
        gift.crowdfunded += amount
        gift.save()
        contribution = Contribution(gift=gift, gift_name= gift.name, gift_pic=gift.pic, contributor_id=contributor_id, contributor_name=contributor_name, contributed_to=contributed_to, contributed_to_name=contributed_to_name, amount=amount, message=message, contribution_date=timestamp, stripe_charge=payment_id)
        contribution.save()
        receiver_session = FacebookSession.objects.get(userID=contributed_to)
        if receiver_session.email:
            send_giftme_email(receiver_session.email, 'You have received a gift contribution!', 'gift_contribution', {'contributor_name': contributor_name, 'gift_name': gift.name, 'gift_amount': amount, 'message': message }, receiver_session.receiveEmails)
        return redirect('/web_pay_process/' + str(gift.id) + '/')
    elif request.method == 'GET':
        context = {'gift_updated': gift}
        return render(request, 'giftme/pay_processed.html', context) 


@csrf_exempt
def notification_of_facebook_share(request):
    if request.method == 'POST':
        userID = request.POST["userID"]
        shareType = request.POST["shareType"]
        try:
            session = FacebookSession.objects.get(userID=userID)
            send_giftme_email('timcallagy@gmail.com', session.name + ': ' + shareType, 'blank', {}, True) 
            return HttpResponse('Success')
        except:
            return HttpResponse('Failure')


def privacy_policy(request):
    context = RequestContext(request)
    if request.method == 'GET':
        return render_to_response('giftme/privacy_policy.html', {}, context) 


################################
###
###  Functions
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

        msg.mixed_subtype = 'related'
        image = open(settings.STATIC_PATH + '/img/logo.png', 'rb')
        msg_img = MIMEImage(image.read())
        image.close()
        msg_img.add_header('Content-ID', 'logo.png')
        msg_img.add_header('From', 'GiftMe')
        msg.attach(msg_img)
        msg.send()
    return

def usd_to_eur_rate():
    exchange_rates = requests.get('https://api.fixer.io/latest?base=USD', headers={'Accept': 'application/json'}).json()
    return exchange_rates["rates"]["EUR"]

def usd_to_eur(usd_amount):
    exchange_rates = requests.get('https://api.fixer.io/latest', headers={'Accept': 'application/json'}).json()
    usd_eur_price = exchange_rates["rates"]["USD"]
    return "{0:.2f}".format(usd_amount/usd_eur_price)

