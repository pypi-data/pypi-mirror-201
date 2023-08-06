import django_tables2 as tables

from netbox.tables import NetBoxTable, columns
from .models import TenantRole, TenantRoleGroup


TENANT_ROLE_LINK = """
{% if record %}
    <a href="{% url 'plugins:netbox_rolesandgroups:tenantrole' pk=record.pk %}">{% firstof record.name record.name %}</a>
{% endif %}
"""

TENANT_ROLE_GROUP_LINK = """
{% if record %}
    <a href="{% url 'plugins:netbox_rolesandgroups:tenantrolegroup' pk=record.pk %}">{% firstof record.name record.name %}</a>
{% endif %}
"""


class TenantRoleTable(NetBoxTable):
    name = tables.TemplateColumn(template_code=TENANT_ROLE_LINK)
    tenant = tables.Column(
        linkify=True
    )
    parent = tables.Column(
        linkify=True
    )

    tags = columns.TagColumn(
        url_name='dcim:sitegroup_list'
    )

    class Meta(NetBoxTable.Meta):
        model = TenantRole
        fields = ('pk', 'id', 'name', 'tenant', 'parent', 'slug', 'comments', 'actions',
                  'created', 'last_updated', 'tags')
        default_columns = ('name', 'tenant', 'parent', 'tags')


class TenantRoleGroupTable(NetBoxTable):
    name = tables.TemplateColumn(template_code=TENANT_ROLE_LINK)
    role = tables.Column(
        linkify=True
    )

    tags = columns.TagColumn(
        url_name='dcim:sitegroup_list'
    )

    class Meta(NetBoxTable.Meta):
        model = TenantRoleGroup
        fields = ('pk', 'id', 'name', 'role', 'slug', 'comments', 'actions',
                  'created', 'last_updated', 'tags')
        default_columns = ('name', 'slug', 'role', 'tags')
