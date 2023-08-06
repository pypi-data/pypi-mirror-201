from extras.plugins import PluginMenuItem, PluginMenu, PluginMenuButton
from utilities.choices import ButtonColorChoices
from django.conf import settings
from django.utils.text import slugify

plugin_settings = settings.PLUGINS_CONFIG.get('netbox_software', {})


class MyPluginMenu(PluginMenu):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = name

    @property
    def name(self):
        return self._name


if plugin_settings.get('enable_navigation_menu'):

    menuitem = []

    # Add a menu item for Device software if enabled
    if plugin_settings.get('enable_device_software'):
        menuitem.append(
            PluginMenuItem(
                link='plugins:netbox_rolesandgroups:tenantrole_list',
                link_text='Роли АИС',
                buttons=[PluginMenuButton(
                    link='plugins:netbox_rolesandgroups:tenantrole_add',
                    title='Создать',
                    icon_class='mdi mdi-plus-thick',
                    color=ButtonColorChoices.GREEN
                )],
                permissions=['tenancy.view_tenant']
            )
        )
        menuitem.append(
            PluginMenuItem(
                link='plugins:netbox_rolesandgroups:tenantrolegroup_list',
                link_text='Группы роей АИС',
                buttons=[PluginMenuButton(
                    link='plugins:netbox_rolesandgroups:tenantrolegroup_add',
                    title='Создать',
                    icon_class='mdi mdi-plus-thick',
                    color=ButtonColorChoices.GREEN
                )],
                permissions=['tenancy.view_tenant']
            )
        )

    # If we are using NB 3.4.0+ display the new top level navigation option
    if settings.VERSION >= '3.4.0':
        menu = MyPluginMenu(
            name='rolesandgroupsPl',
            label='Роли АИС',
            groups=(
                ('Программы', menuitem),
            ),
            icon_class='mdi mdi-account-group'
        )

    else:

        # Fall back to pre 3.4 navigation option
        menu_items = menuitem
