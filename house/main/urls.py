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
    url(r'^(?P<slug>[-\w]+)/photos/(?P<pk>\d+)/$',
        views.photo,
        name='photo'),
    url(r'^(?P<slug>[-\w]+)/photos/upload/$',
        views.photos_upload,
        name='photos.upload'),
    url(r'^(?P<slug>[-\w]+)/documents/$',
        views.documents,
        name='documents'),
    url(r'^(?P<slug>[-\w]+)/documents/(?P<pk>\d+)/download$',
        views.document_download,
        name='document_download'),
    url(r'^(?P<slug>[-\w]+)/documents/upload/$',
        views.documents_upload,
        name='documents.upload'),
    url(r'^(?P<slug>[-\w]+)/accounts/$',
        views.accounts,
        name='accounts'),
    url(r'^(?P<slug>[-\w]+)/accounts/sendagain/(?P<identifier>\w+)/$',
        views.send_again,
        name='send_again'),
    url(r'^(?P<slug>[-\w]+)/accounts/accept/(?P<identifier>\w+)/$',
        views.accept_invitation,
        name='accept_invitation'),
)
