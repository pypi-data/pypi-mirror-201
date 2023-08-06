import django_tables2 as tables

from netbox.tables import NetBoxTable, columns
from .models import DeviceSoftware


DEVICE_SOFTWARE_LINK = """
{% if record %}
    <a href="{% url 'plugins:netbox_software:devicesoftware' pk=record.pk %}">{% firstof record.name record.name %}</a>
{% endif %}
"""


class DeviceSoftwareTable(NetBoxTable):
    name = tables.TemplateColumn(template_code=DEVICE_SOFTWARE_LINK)
    software_type = columns.ChoiceFieldColumn()
    device = tables.Column(
        linkify=True
    )

    tags = columns.TagColumn(
        url_name='dcim:sitegroup_list'
    )

    class Meta(NetBoxTable.Meta):
        model = DeviceSoftware
        fields = ('pk', 'id', 'name', 'software_type',  'source', 'version', 'device', 'comments', 'actions',
                  'created', 'last_updated', 'tags')
        default_columns = ('name', 'software_type', 'device', 'tags')
