from netbox.search import SearchIndex
from .models import TenantRole, TenantRoleGroup
from django.conf import settings

# If we run NB 3.4+ register search indexes 
if settings.VERSION >= '3.4.0':
    class TenantRoleIndex(SearchIndex):
        model = TenantRole
        fields = (
            ("name", 100),
            ("slug", 500),
            ("comments", 5000),
        )

    class TenantRoleGroupIndex(SearchIndex):
        model = TenantRoleGroup
        fields = (
            ("name", 100),
            ("slug", 500),
            ("comments", 5000),
        )

    # Register indexes
    indexes = [TenantRoleIndex, TenantRoleGroupIndex]
