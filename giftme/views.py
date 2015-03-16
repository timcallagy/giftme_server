from django.template import RequestContext
from django.http import HttpResponse

def add_item(request):
    context = RequestContext(request)
    if request.method == 'POST':
        return HttpResponse('true')
    else:
        return HttpResponse('true')
