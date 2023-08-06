from extras.plugins import PluginMenuItem, PluginMenu, PluginMenuButton
from utilities.choices import ButtonColorChoices
from django.conf import settings

plugin_settings = settings.PLUGINS_CONFIG.get('netbox_software', {})

if plugin_settings.get('enable_navigation_menu'):

    menuitem = []

    # Add a menu item for Device software if enabled
    if plugin_settings.get('enable_device_software'):
        menuitem.append(
            PluginMenuItem(
                link='plugins:netbox_software:devicesoftware_list',
                link_text='Устройства',
                buttons=[PluginMenuButton(
                    link='plugins:netbox_software:devicesoftware_add',
                    title='Создать',
                    icon_class='mdi mdi-plus-thick',
                    color=ButtonColorChoices.GREEN
                )],
                permissions=['dcim.view_device']
            )
        )

    # If we are using NB 3.4.0+ display the new top level navigation option
    if settings.VERSION >= '3.4.0':

        menu = PluginMenu(
            label='Установленное ПО',
            groups=(
                ('Программы', menuitem),
            ),
            icon_class='mdi mdi-file-software-multiple'
        )

    else:

        # Fall back to pre 3.4 navigation option
        menu_items = menuitem
