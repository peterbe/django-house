from house.base.forms import BaseForm, BaseModelForm
from house.main import models


class HouseForm(BaseModelForm):

    class Meta:
        model = models.House
        fields = ('name',)


class AddressForm(BaseModelForm):

    class Meta:
        model = forms.Address
        fields = ('line1', 'line2', 'state', 'zip_code', 'country',)
