from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^entrar/$', auth_views.login, {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^registrar/$', views.register, name='register'),
]
