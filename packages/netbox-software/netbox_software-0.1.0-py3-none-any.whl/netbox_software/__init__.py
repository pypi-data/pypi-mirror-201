from extras.plugins import PluginConfig


class NetboxSoftware(PluginConfig):
    name = 'netbox-software'
    verbose_name = 'Roles Storage'
    description = 'Manage device software in Netbox'
    version = '0.1.0'
    author = 'Ilya Zakharov'
    author_email = 'me@izakharov.ru'
    min_version = '3.2.0'
    base_url = 'documents'
    default_settings = {
        "enable_device_software": True,
        "device_software_location": "left",
    }


config = NetboxSoftware
