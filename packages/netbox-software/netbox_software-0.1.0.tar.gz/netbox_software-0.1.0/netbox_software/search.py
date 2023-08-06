from netbox.search import SearchIndex
from .models import DeviceSoftware
from django.conf import settings

# If we run NB 3.4+ register search indexes 
if settings.VERSION >= '3.4.0':
    class DeviceSoftwareIndex(SearchIndex):
        model = DeviceSoftware
        fields = (
            ("name", 100),
            ("source", 500),
            ("comments", 5000),
        )

    # Register indexes
    indexes = [DeviceSoftwareIndex]
