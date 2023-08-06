from django.urls import path
from . import models, views
from netbox.views.generic import ObjectChangeLogView

urlpatterns = (

    # TenantRole
    path('tenant-roles/', views.TenantRoleListView.as_view(), name='tenantrole_list'),
    path('tenant-roles/add/', views.TenantRoleEditView.as_view(), name='tenantrole_add'),
    path('tenant-roles/<int:pk>/', views.TenantRoleView.as_view(), name='tenantrole'),
    path('tenant-roles/<int:pk>/edit/', views.TenantRoleEditView.as_view(), name='tenantrole_edit'),
    path('tenant-roles/<int:pk>/delete/', views.TenantRoleDeleteView.as_view(), name='tenantrole_delete'),
    path('tenant-roles/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='tenantrole_changelog', kwargs={
        'model': models.TenantRole
    }),
    
    # TenantRoleGroup
    path('tenant-rolegroups/', views.TenantRoleGroupListView.as_view(), name='tenantrolegroup_list'),
    path('tenant-rolegroups/add/', views.TenantRoleGroupEditView.as_view(), name='tenantrolegroup_add'),
    path('tenant-rolegroups/<int:pk>/', views.TenantRoleGroupView.as_view(), name='tenantrolegroup'),
    path('tenant-rolegroups/<int:pk>/edit/', views.TenantRoleGroupEditView.as_view(), name='tenantrolegroup_edit'),
    path('tenant-rolegroups/<int:pk>/delete/', views.TenantRoleGroupDeleteView.as_view(), name='tenantrolegroup_delete'),
    path('tenant-rolegroups/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='tenantrolegroup_changelog', kwargs={
        'model': models.TenantRoleGroup
    }),  

)
