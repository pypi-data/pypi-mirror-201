from netbox.api.viewsets import NetBoxModelViewSet

from .. import models, filtersets
from .serializers import TenantRoleSerializer, TenantRoleGroupSerializer


class TenantRoleViewSet(NetBoxModelViewSet):
    queryset = models.TenantRole.objects.prefetch_related('tags')
    serializer_class = TenantRoleSerializer
    filterset_class = filtersets.TenantRoleFilterSet


class TenantRoleGroupViewSet(NetBoxModelViewSet):
    queryset = models.TenantRoleGroup.objects.prefetch_related('tags')
    serializer_class = TenantRoleGroupSerializer
    filterset_class = filtersets.TenantRoleGroupFilterSet
