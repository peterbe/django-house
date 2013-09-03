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
