from netbox.filtersets import NetBoxModelFilterSet
from .models import DeviceSoftware
from django.db.models import Q


class DeviceSoftwareFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = DeviceSoftware
        fields = ('id', 'name', 'software_type', 'device')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(version__icontains=value)
        )
