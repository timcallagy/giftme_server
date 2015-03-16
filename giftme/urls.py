from django.conf.urls import url, patterns
from giftme import views

urlpatterns = patterns('',
        url(r'^add_item/$', views.add_item),
)
