from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^victim', views.index, name='index'),
    url(r'^form', views.form, name='form'),
]
