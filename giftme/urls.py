from django.conf.urls import url, patterns
from giftme import views

urlpatterns = patterns('',
        url(r'^add_gift/$', views.add_gift),
        url(r'^get_csrf_token/$', views.get_csrf_token),
)
