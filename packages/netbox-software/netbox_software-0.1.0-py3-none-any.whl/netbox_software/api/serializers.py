from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from ..models import DeviceSoftware
from dcim.api.nested_serializers import NestedDeviceSerializer


# Device Software Serializer
class DeviceSoftwareSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netboxsoftware-api:devicesoftware-detail'
    )

    device = NestedDeviceSerializer()

    class Meta:
        model = DeviceSoftware
        fields = (
            'id', 'url', 'display', 'name', 'software_type', 'source', 'version', 'device', 'comments', 'tags',
            'custom_fields', 'created', 'last_updated',
        )


class NestedDeviceSoftwareSerializer(WritableNestedSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netboxsoftware-api:devicesoftware-detail'
    )

    class Meta:
        model = DeviceSoftware
        fields = (
            'id', 'url', 'display', 'name', 'software_type', 'source', 'version',
        )
