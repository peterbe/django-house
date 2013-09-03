from django import http
from django.core.urlresolvers import reverse
from django.utils.timezone import utc
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db import transaction

from . import models
from . import forms


def robots_txt(request):
    return http.HttpResponse(
        'User-agent: *\n'
        '%s: /' % ('Allow' if settings.ENGAGE_ROBOTS else 'Disallow'),
        mimetype='text/plain',
    )


def start(request):
    context = {'house': None}
    if request.user.is_authenticated():
        for house in models.House.objects.filter(owners=request.user):
            context['house'] = house
    return render(request, 'main/start.html', context)


@login_required
def home(request, slug):
    context = {}
    house = get_object_or_404(models.House, slug=slug, owners=request.user)
    context['house'] = house
    context['page_title'] = house.name
    return render(request, 'main/home.html', context)


@login_required
def photos(request, slug):
    context = {}
    house = get_object_or_404(models.House, slug=slug, owners=request.user)
    context['house'] = house
    context['page_title'] = 'Photos for %s' % house.name
    return render(request, 'main/photos.html', context)


@login_required
def photos_upload(request, slug):
    context = {}
    house = get_object_or_404(models.House, slug=slug, owners=request.user)


@login_required
def documents(request, slug):
    context = {}
    house = get_object_or_404(models.House, slug=slug, owners=request.user)
    context['house'] = house
    context['page_title'] = 'Documents for %s' % house.name
    return render(request, 'main/documents.html', context)


@login_required
@transaction.commit_on_success
def address(request, slug):
    context = {}
    house = get_object_or_404(models.House, slug=slug, owners=request.user)
    context['house'] = house
    if request.method == 'POST':
        form = forms.AddressForm(data=request.POST, instance=house.address)
        if form.is_valid():
            form.save()
            return redirect('main:home', house.slug)
    else:
        form = forms.AddressForm(instance=house.address)
    context['form'] = form
    for field in form.fields:
        form.fields[field].widget.attrs['class'] = 'pure-input-1-3'
    return render(request, 'main/address.html', context)
