from giftme.forms import GiftForm
from giftme.models import Gift
from django.template import RequestContext
from django.http import HttpResponse
from django.middleware.csrf import _get_new_csrf_key as get_new_csrf_key
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from django.core.serializers.json import DjangoJSONEncoder

def get_csrf_token(request):
    csrftoken = get_new_csrf_key()
    return HttpResponse(csrftoken)

@csrf_exempt
def add_gift(request):
    context = RequestContext(request)
    if request.method == 'POST':
        add_gift_form = GiftForm(data=request.POST)
        if add_gift_form.is_valid():
            gift = add_gift_form.save()
            return HttpResponse('true')
        else:
            return HttpResponse('false')
    else:
        return HttpResponse('false')

def get_gifts(request, id):
    gifts = Gift.objects.filter(owner_id = id );
    data = serializers.serialize('json', gifts)
    return HttpResponse(data)

@csrf_exempt
def delete_gift(request, pk):
    Gift.objects.get(pk=pk).delete()
    return HttpResponse()

