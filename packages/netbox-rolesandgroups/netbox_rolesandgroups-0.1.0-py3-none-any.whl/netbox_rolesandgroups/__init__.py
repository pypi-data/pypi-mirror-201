from extras.plugins import PluginConfig


class NetboxRolesAndGroupse(PluginConfig):
    name = 'netbox_rolesandgroups'
    verbose_name = 'Роли и группы АИС'
    description = 'Manage rolesandgroups for tenants in Netbox'
    version = '0.1.0'
    author = 'Ilya Zakharov'
    author_email = 'me@izakharov.ru'
    min_version = '3.2.0'
    base_url = 'rolesandgroups'
    default_settings = {
        "enable_navigation_menu": True,
        "enable_tenant_rolesandgroups": True,
        "tenant_rolesandgroups_location": "left",
    }


config = NetboxRolesAndGroupse
