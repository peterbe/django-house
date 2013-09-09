from django import forms
from django.forms import widgets
from house.base.forms import BaseForm, BaseModelForm
from . import models


class AddressForm(BaseModelForm):

    class Meta:
        model = models.Address
        fields = (
            'line1', 'line2', 'zip_code', 'city', 'state', 'country',
            'latitude', 'longitude',
        )

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.fields['latitude'].widget = widgets.HiddenInput()
        self.fields['longitude'].widget = widgets.HiddenInput()


class PhotoUploadForm(BaseForm):

    url = forms.URLField(widget=widgets.HiddenInput())


class InviteForm(BaseForm):

    email_address = forms.EmailField()
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    message = forms.CharField(required=False, widget=widgets.Textarea())
