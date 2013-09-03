from django import http
from django.core.urlresolvers import reverse
from django.utils.timezone import utc
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db import transaction
from django.template.defaultfilters import slugify

from house.main import forms
from house.main import models


def start(request):
    context = {}
    return render(request, 'signin/start.html', context)


def failed(request):
    pass


def loggedout(request):
    pass


@login_required
@transaction.commit_on_success
def register(request):
    context = {}
    if request.method == 'POST':
        form = forms.AddressForm(request.POST)
        if form.is_valid():
            address = form.save()
            house = models.House.objects.create(
                name=address.line1,
                slug=slugify(address.line1),
                address=address,
            )
            house.owners.add(request.user)
            url = reverse('signin:done')
            return redirect(url)
    else:
        initial = {'country': 'United States'}
        form = forms.AddressForm(initial=initial)
    context['form'] = form
    form.fields['line1'].label = 'Adress line 1'
    form.fields['line2'].label = 'Adress line 2 (optional)'
    for field in form.fields:
        form.fields[field].widget.attrs['class'] = 'pure-input-1-3'
    return render(request, 'signin/register.html', context)


@login_required
def done(request):
    context = {}
    context['house'] = models.House.get_house(request.user)
    return render(request, 'signin/done.html', context)


def account(request):
    pass
