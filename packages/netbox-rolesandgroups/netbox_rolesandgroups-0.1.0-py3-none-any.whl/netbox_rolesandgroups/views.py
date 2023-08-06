from django.contrib.auth.mixins import PermissionRequiredMixin
from netbox.views import generic
from . import forms, models, tables, filtersets


### TenantRole
class TenantRoleView(PermissionRequiredMixin, generic.ObjectView):
    permission_required = ('tenancy.view_tenant',)
    queryset = models.TenantRole.objects.all()


class TenantRoleListView(PermissionRequiredMixin, generic.ObjectListView):
    permission_required = ('tenancy.view_tenant',)
    queryset = models.TenantRole.objects.all()
    table = tables.TenantRoleTable
    filterset = filtersets.TenantRoleFilterSet
    filterset_form = forms.TenantRoleFilterForm


class TenantRoleEditView(PermissionRequiredMixin, generic.ObjectEditView):
    permission_required = ('tenancy.view_tenant',)
    queryset = models.TenantRole.objects.all()
    form = forms.TenantRoleForm

    template_name = 'netbox_rolesandgroups/tenantrole_edit.html'


class TenantRoleDeleteView(PermissionRequiredMixin, generic.ObjectDeleteView):
    permission_required = ('tenancy.view_tenant',)
    queryset = models.TenantRole.objects.all()


### TenantRoleGroup
class TenantRoleGroupView(PermissionRequiredMixin, generic.ObjectView):
    permission_required = ('tenancy.view_tenant',)
    queryset = models.TenantRoleGroup.objects.all()


class TenantRoleGroupListView(PermissionRequiredMixin, generic.ObjectListView):
    permission_required = ('tenancy.view_tenant',)
    queryset = models.TenantRoleGroup.objects.all()
    table = tables.TenantRoleGroupTable
    filterset = filtersets.TenantRoleGroupFilterSet
    filterset_form = forms.TenantRoleGroupFilterForm


class TenantRoleGroupEditView(PermissionRequiredMixin, generic.ObjectEditView):
    permission_required = ('tenancy.view_tenant',)
    queryset = models.TenantRoleGroup.objects.all()
    form = forms.TenantRoleGroupForm

    template_name = 'netbox_rolesandgroups/tenantrolegroup_edit.html'


class TenantRoleGroupDeleteView(PermissionRequiredMixin, generic.ObjectDeleteView):
    permission_required = ('tenancy.view_tenant',)
    queryset = models.TenantRoleGroup.objects.all()
