from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^entrar/$', auth_views.login, {'template_name': 'accounts/login.html'}, name='login'),
    # url(r'^registrar/$', auth_views.register, {'template_name': 'accounts/register.html'}, name='register'),
]
