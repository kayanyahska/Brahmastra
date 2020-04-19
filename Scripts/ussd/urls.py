from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^ussd/$', views.index, name='index'),
    url(r'^ussdrelief/$', views.ussdrelief, name='ussdrelief'),
    url(r'^sms/$',views.sms, name='sms'),
    url(r'^location/$',views.location, name='location'),
    url(r'^locationv/$',views.locationv, name='location')
]