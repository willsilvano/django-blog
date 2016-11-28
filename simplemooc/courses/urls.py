from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^(?P<id>\d+)/$', views.details, name='details'),
    url(r'^(?P<slug>[\w_-]+)/$', views.details, name='details'),
]
