from netbox.filtersets import NetBoxModelFilterSet
from .models import TenantRole, TenantRoleGroup
from django.db.models import Q


class TenantRoleFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = TenantRole
        fields = ('id', 'name', 'slug', 'tenant', 'parent')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(slug__icontains=value)
        )


class TenantRoleGroupFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = TenantRoleGroup
        fields = ('id', 'name', 'slug', 'role')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(slug__icontains=value)
        )
