# radar/urls.py

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^815/$', views.etl, name='etl'),
    url(r'^rate/$', views.exchangerate, name='rate'),
    url(r'^task/(?P<id>\w+)$', views.view_task, name='view_task'),
]