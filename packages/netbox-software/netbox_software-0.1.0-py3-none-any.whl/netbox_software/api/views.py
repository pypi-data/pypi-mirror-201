from netbox.api.viewsets import NetBoxModelViewSet

from .. import models, filtersets
from .serializers import DeviceSoftwareSerializer


class DeviceSoftwareViewSet(NetBoxModelViewSet):
    queryset = models.DeviceSoftware.objects.prefetch_related('tags')
    serializer_class = DeviceSoftwareSerializer
    filterset_class = filtersets.DeviceSoftwareFilterSet
