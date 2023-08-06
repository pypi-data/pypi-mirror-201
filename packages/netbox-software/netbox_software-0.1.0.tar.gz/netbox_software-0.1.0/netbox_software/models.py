from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet


class DeviceSoftTypeChoices(ChoiceSet):

    key = 'SoftTypeChoices.device'

    CHOICES = [
        ('py_package', 'Package (Python)', 'green'),
        ('deb_package', 'Package (deb)', 'pink'),
        ('win_program', 'Program (Windows)', 'orange'),
        ('brow_plugin', 'Browser plugin (IE)', 'indigo'),
        ('rpm_package', 'Package (rpm)', 'blue'),
        ('other', 'Прочее', 'gray'),
    ]


class DeviceSoftware(NetBoxModel):
    name = models.CharField(
        verbose_name="название",
        max_length=100,
        unique=True,
        help_text='Укажите имя, которое будет отображаться для этого ПО.'
    )

    software_type = models.CharField(
        verbose_name="тип ПО",
        max_length=30,
        choices=DeviceSoftTypeChoices
    )

    device = models.ForeignKey(
        verbose_name="устройство",
        to='dcim.Device',
        on_delete=models.CASCADE,
        related_name='software'
    )

    source = models.CharField(
        verbose_name="источник",
        max_length=100,
        blank=True
    )

    version = models.CharField(
        verbose_name="версия",
        max_length=50,
        blank=True
    )

    comments = models.TextField(
        verbose_name="комментарий",
        blank=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "ПО устройств"
        verbose_name = "ПО устройства"

    def get_document_type_color(self):
        return DeviceSoftTypeChoices.colors.get(self.software_type)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_software:devicesoftware', args=[self.pk])
