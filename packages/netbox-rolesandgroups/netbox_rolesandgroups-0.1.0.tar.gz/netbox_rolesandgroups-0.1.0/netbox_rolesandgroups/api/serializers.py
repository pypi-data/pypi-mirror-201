from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from ..models import TenantRole, TenantRoleGroup
from tenancy.api.nested_serializers import NestedTenantSerializer


# Tenant Role Serializer
class NestedTenantRoleSerializer(WritableNestedSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_rolesandgroups-api:tenantrole-detail'
    )

    class Meta:
        model = TenantRole
        fields = (
            'id', 'url', 'display', 'name', 'slug',
        )


class TenantRoleSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_rolesandgroups-api:tenantrole-detail'
    )

    tenant = NestedTenantSerializer()
    parent = NestedTenantRoleSerializer()

    class Meta:
        model = TenantRole
        fields = (
            'id', 'url', 'display', 'name', 'slug', 'tenant', 'parent', 'comments', 'tags',
            'custom_fields', 'created', 'last_updated',
        )


# Tenant Role Group  Serializer
class TenantRoleGroupSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_rolesandgroups-api:tenantrolegroup-detail'
    )

    role = NestedTenantRoleSerializer()

    class Meta:
        model = TenantRoleGroup
        fields = (
            'id', 'url', 'display', 'name', 'slug', 'role', 'comments', 'tags',
            'custom_fields', 'created', 'last_updated',
        )


class NestedTenantRoleGroupSerializer(WritableNestedSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_rolesandgroups-api:tenantrolegroup-detail'
    )

    class Meta:
        model = TenantRoleGroup
        fields = (
            'id', 'url', 'display', 'name', 'slug',
        )

