from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from dcim.models import Device
from utilities.forms import TagFilterField, CommentField, DynamicModelChoiceField
from .models import DeviceSoftware, DeviceSoftTypeChoices


# Device Software Form & Filter Form
class DeviceSoftwareForm(NetBoxModelForm):
    comments = CommentField()

    device = DynamicModelChoiceField(
        label='Устройство',
        queryset=Device.objects.all()
    )

    class Meta:
        model = DeviceSoftware
        fields = ('name', 'software_type', 'device', 'source', 'version', 'comments', 'tags')


class DeviceSoftwareFilterForm(NetBoxModelFilterSetForm):
    model = DeviceSoftware

    name = forms.CharField(
        label='Название',
        required=False
    )

    device = forms.ModelMultipleChoiceField(
        label='Устройство',
        queryset=Device.objects.all(),
        required=False
    )

    software_type = forms.MultipleChoiceField(
        label='software_type',
        choices=DeviceSoftTypeChoices,
        required=False
    )

    tag = TagFilterField(model)
