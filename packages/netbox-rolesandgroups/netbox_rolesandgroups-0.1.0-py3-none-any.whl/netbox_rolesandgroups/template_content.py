from extras.plugins import PluginTemplateExtension
from django.conf import settings
from .models import TenantRole, TenantRoleGroup

plugin_settings = settings.PLUGINS_CONFIG.get('netbox_rolesandgroups', {})


class TenantRoleList(PluginTemplateExtension):
    model = 'tenancy.tenant'

    def left_page(self):
        if plugin_settings.get('enable_device_software') and plugin_settings.get('device_software_location') == 'left':

            return self.render('netbox_rolesandgroups/tenantrole_include.html', extra_context={
                'tenant_roles': TenantRole.objects.filter(device=self.context['object']),
            })
        else:
            return ""

    def right_page(self):
        if plugin_settings.get('enable_device_software') and plugin_settings.get('device_software_location') == 'right':

            return self.render('netbox_rolesandgroups/tenantrole_include.html', extra_context={
                'tenant_roles': TenantRole.objects.filter(device=self.context['object']),
            })
        else:
            return ""


class TenantRoleGroupList(PluginTemplateExtension):
    model = 'netbox_rolesandgroups:tenantrole'

    def left_page(self):
        if plugin_settings.get('enable_device_software') and plugin_settings.get('device_software_location') == 'left':

            return self.render('netbox_rolesandgroups/tenantrolegroup_include.html', extra_context={
                'tenant_rolegroups': TenantRoleGroup.objects.filter(device=self.context['object']),
            })
        else:
            return ""

    def right_page(self):
        if plugin_settings.get('enable_device_software') and plugin_settings.get('device_software_location') == 'right':

            return self.render('netbox_rolesandgroups/tenantrolegroup_include.html', extra_context={
                'tenant_rolegroups': TenantRoleGroup.objects.filter(device=self.context['object']),
            })
        else:
            return ""


template_extensions = [TenantRoleList, TenantRoleGroupList]
