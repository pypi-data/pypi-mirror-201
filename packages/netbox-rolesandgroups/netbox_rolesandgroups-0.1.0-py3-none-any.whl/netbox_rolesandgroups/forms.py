from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from tenancy.models import Tenant
from utilities.forms import TagFilterField, CommentField, DynamicModelChoiceField
from .models import TenantRole, TenantRoleGroup


# Tenant Role Form & Filter Form
class TenantRoleForm(NetBoxModelForm):
    comments = CommentField()

    tenant = DynamicModelChoiceField(
        label='АИС',
        queryset=Tenant.objects.all()
    )

    parent = DynamicModelChoiceField(
        label='Роль',
        queryset=TenantRole.objects.all()
    )

    class Meta:
        model = TenantRole
        fields = ('name', 'slug', 'tenant', 'parent', 'comments', 'tags')


class TenantRoleFilterForm(NetBoxModelFilterSetForm):
    model = TenantRole

    name = forms.CharField(
        label='Название',
        required=False
    )

    slug = forms.CharField(
        label='короткий URL',
        required=False
    )

    tenant = forms.ModelMultipleChoiceField(
        label='АИС',
        queryset=Tenant.objects.all(),
        required=False
    )

    parent = forms.ModelMultipleChoiceField(
        label='Роль',
        queryset=TenantRole.objects.all(),
        required=False
    )

    tag = TagFilterField(model)


# Tenant Role Group Form & Filter Form
class TenantRoleGroupForm(NetBoxModelForm):
    comments = CommentField()

    role = DynamicModelChoiceField(
        label='Роль',
        queryset=TenantRole.objects.all()
    )

    class Meta:
        model = TenantRoleGroup
        fields = ('name', 'slug', 'role', 'comments', 'tags')


class TenantRoleGroupFilterForm(NetBoxModelFilterSetForm):
    model = TenantRoleGroup

    name = forms.CharField(
        label='Название',
        required=False
    )

    slug = forms.CharField(
        label='короткий URL',
        required=False
    )

    role = forms.ModelMultipleChoiceField(
        label='Роль',
        queryset=TenantRole.objects.all(),
        required=False
    )

    tag = TagFilterField(model)
