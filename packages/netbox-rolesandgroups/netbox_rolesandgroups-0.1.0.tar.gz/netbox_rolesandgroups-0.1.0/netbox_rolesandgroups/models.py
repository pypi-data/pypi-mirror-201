from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet


class TenantRole(NetBoxModel):
    name = models.CharField(
        verbose_name="название",
        max_length=100,
        unique=True,
        help_text='Укажите имя, которое будет отображаться для этой рооли.'
    )

    slug = models.SlugField(
        verbose_name="короткий URL",
        max_length=100,
        unique=True
    )

    tenant = models.ForeignKey(
        verbose_name="устройство",
        to='tenancy.Tenant',
        on_delete=models.CASCADE,
        related_name='tenant_role'
    )

    parent = models.ForeignKey(
        verbose_name="Группа",
        to='self',
        on_delete=models.SET_NULL,
        related_name='role',
        blank=True,
        null=True
    )

    comments = models.TextField(
        verbose_name="комментарий",
        blank=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Роли АИС"
        verbose_name = "Роль АИС"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_rolesandgroups:tenantrole', args=[self.pk])


class TenantRoleGroup(NetBoxModel):
    name = models.CharField(
        verbose_name="название",
        max_length=100,
        unique=True,
        help_text='Укажите имя, которое будет отображаться для этой группы.'
    )

    slug = models.SlugField(
        verbose_name="короткий URL",
        max_length=100,
        unique=True
    )

    role = models.ForeignKey(
        verbose_name="роль",
        to=TenantRole,
        on_delete=models.CASCADE,
        related_name='role_group',
        blank=True,
        null=True
    )

    comments = models.TextField(
        verbose_name="комментарий",
        blank=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Группы ролей АИС"
        verbose_name = "Группа роли АИС"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_rolesandgroups:tenantrolegroup', args=[self.pk])
