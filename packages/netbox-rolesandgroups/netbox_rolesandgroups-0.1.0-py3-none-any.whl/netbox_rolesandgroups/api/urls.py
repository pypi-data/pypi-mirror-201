from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'netbox_rolesandgroups'

router = NetBoxRouter()
router.register('tenant-roles', views.TenantRoleViewSet)
router.register('tenant-roles-groups', views.TenantRoleGroupViewSet)

urlpatterns = router.urls
