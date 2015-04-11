from django.conf.urls import url, patterns
from giftme import views

urlpatterns = patterns('',
        url(r'^login/$', views.login),
        url(r'^wakeup/$', views.wakeup),
        url(r'^get_csrf_token/$', views.get_csrf_token),
        url(r'^add_gift/$', views.add_gift),
        url(r'^get_gifts/(?P<id>[0-9]+)/$', views.get_gifts),
        url(r'^get_gift/(?P<pk>[0-9]+)/$', views.get_gift),
        url(r'^get_friends_gifts/(?P<id>[0-9]+)/$', views.get_friends_gifts),
        url(r'^delete_gift/(?P<pk>[0-9]+)/$', views.delete_gift),
        url(r'^pay/(?P<pk>[0-9]+)/$', views.pay),
        url(r'^get_contributions/(?P<pk>[0-9]+)/$', views.get_contributions),
        url(r'^settings/(?P<id>[0-9]+)/$', views.settings),
)
