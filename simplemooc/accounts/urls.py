from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^entrar/$', auth_views.login, {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^sair/$', auth_views.logout, {'next_page': 'core:home'}, name='logout'),
    url(r'^cadastre-se/$', views.register, name='register'),
    url(r'^editar/$', views.edit, name='edit'),
]
