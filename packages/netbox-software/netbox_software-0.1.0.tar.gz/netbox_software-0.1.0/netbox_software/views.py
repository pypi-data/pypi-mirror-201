from django.contrib.auth.mixins import PermissionRequiredMixin
from netbox.views import generic
from . import forms, models, tables, filtersets


### DeviceSoftware
class DeviceSoftwareView(PermissionRequiredMixin, generic.ObjectView):
    permission_required = ('dcim.view_site', 'dcim.view_device')
    queryset = models.DeviceSoftware.objects.all()


class DeviceSoftwareListView(PermissionRequiredMixin, generic.ObjectListView):
    permission_required = ('dcim.view_site', 'dcim.view_device')
    queryset = models.DeviceSoftware.objects.all()
    table = tables.DeviceSoftwareTable
    filterset = filtersets.DeviceSoftwareFilterSet
    filterset_form = forms.DeviceSoftwareFilterForm


class DeviceSoftwareEditView(PermissionRequiredMixin, generic.ObjectEditView):
    permission_required = ('dcim.view_site', 'dcim.view_device')
    queryset = models.DeviceSoftware.objects.all()
    form = forms.DeviceSoftwareForm

    template_name = 'netbox_documents/devicesoftware_edit.html'


class DeviceSoftwareDeleteView(PermissionRequiredMixin, generic.ObjectDeleteView):
    permission_required = ('dcim.view_site', 'dcim.view_device')
    queryset = models.DeviceSoftware.objects.all()
