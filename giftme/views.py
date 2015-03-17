from giftme.forms import GiftForm
from django.template import RequestContext
from django.http import HttpResponse
from django.middleware.csrf import _get_new_csrf_key as get_new_csrf_key
from django.views.decorators.csrf import csrf_exempt

def get_csrf_token(request):
    """
    response = HttpResponse(request)
    response.set_cookie("csrftoken", get_new_csrf_key())
    return response
    """
    context = RequestContext(request)
    print(context)
    csrftoken = get_new_csrf_key()
    return HttpResponse(csrftoken)

@csrf_exempt
def add_gift(request):
    context = RequestContext(request)
    if request.method == 'POST':
        add_gift_form = GiftForm(data=request.POST)
        print(add_gift_form)
        if add_gift_form.is_valid():
            gift = add_gift_form.save()
            return HttpResponse('true')
        else:
            print('invalid')
            return HttpResponse('false')
    else:
        return HttpResponse('false')
