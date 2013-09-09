from django import http
from django.core.urlresolvers import reverse
from django.utils.timezone import utc
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db import transaction
from django.core.mail import send_mail

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
    context['house'] = house
    context['page_title'] = 'Photo upload'
    form = forms.PhotoUploadForm()
    context['form'] = form
    context['filepicker_api_key'] = settings.FILEPICKER_API_KEY
    return render(request, 'main/photos_upload.html', context)


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


@login_required
@transaction.commit_on_success
def accounts(request, slug):
    context = {}
    house = get_object_or_404(models.House, slug=slug, owners=request.user)
    context['house'] = house
    context['page_title'] = 'Accounts'
    if request.method == 'POST':
        form = forms.InviteForm(request.POST)
        if form.is_valid():
            invitation = models.Invitation.objects.create(
                house=house,
                user=request.user,
                email_address=form.cleaned_data['email_address'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                message=form.cleaned_data['message'],
            )
            send_invite(invitation, request)
            invitation.send_date = models.now()
            invitation.save()
            return redirect('main:accounts', house.slug)
    else:
        form = forms.InviteForm()
    for field in form.fields:
        form.fields[field].widget.attrs['class'] = 'pure-input-1-3'
        placeholder = ''
        form.fields[field].widget.attrs['placeholder'] = placeholder
    context['form'] = form
    return render(request, 'main/accounts.html', context)


def send_invite(invitation, request):
    context = {
        'invitation': invitation,
    }
    body = render_to_string('main/_invitation.txt', context)
    subject = 'Invitation to manage %s' % house.name
    send_email(
        subject,
        body,
        settings.WEBMASTER_FROM,
        [invitation.email_address],
        reply_to=invitation.user.email
    )
