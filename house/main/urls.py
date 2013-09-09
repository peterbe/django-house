from django.conf.urls import patterns, url, include

from . import views

urlpatterns = patterns(
    '',
    url('^robots\.txt$',
        views.robots_txt,
        name='robots_txt'),
    url(r'^$',
        views.start,
        name='start'),
    url(r'^(?P<slug>[-\w]+)/$',
        views.home,
        name='home'),
    url(r'^(?P<slug>[-\w]+)/address/$',
        views.address,
        name='address'),
    url(r'^(?P<slug>[-\w]+)/photos/$',
        views.photos,
        name='photos'),
    url(r'^(?P<slug>[-\w]+)/photos/upload/$',
        views.photos_upload,
        name='photos.upload'),
    url(r'^(?P<slug>[-\w]+)/documents/$',
        views.documents,
        name='documents'),
    url(r'^(?P<slug>[-\w]+)/accounts/$',
        views.accounts,
        name='accounts'),
)
