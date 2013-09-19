from django.conf.urls import patterns, url, include

from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.start,
        name='start'),
    url(r'^failed/$', views.failed,
        name='failed'),
    url(r'^register/$', views.register,
        name='register'),
    url(r'^register/done/$', views.done,
        name='done'),
    url(r'^account/$', views.account,
        name='account'),
    url(r'^signout/$', views.signout,
        name='signout'),
    url(r'^signedout/$', views.signedout,
        name='signedout'),
)
