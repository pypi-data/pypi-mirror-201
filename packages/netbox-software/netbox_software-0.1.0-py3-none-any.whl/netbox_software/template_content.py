from extras.plugins import PluginTemplateExtension
from django.conf import settings
from .models import DeviceSoftware

plugin_settings = settings.PLUGINS_CONFIG.get('netbox_software', {})


class DeviceSoftwareList(PluginTemplateExtension):
    model = 'dcim.device'

    def left_page(self):
        if plugin_settings.get('enable_device_software') and plugin_settings.get('device_software_location') == 'left':

            return self.render('netbox_software/devicesoftware_include.html', extra_context={
                'device_software': DeviceSoftware.objects.filter(device=self.context['object']),
            })
        else:
            return ""

    def right_page(self):
        if plugin_settings.get('enable_device_software') and plugin_settings.get('device_software_location') == 'right':

            return self.render('netbox_software/devicesoftware_include.html', extra_context={
                'device_software': DeviceSoftware.objects.filter(device=self.context['object']),
            })
        else:
            return ""


template_extensions = [DeviceSoftwareList]
