from django.db.models.signals import post_save
from django.dispatch import receiver
from acl.models.acl import AccessControlList
from acl.utils import collect_default_permissions
from structure.models import Organization
from django.utils.translation import gettext_lazy as _


def create_acl(name: str, owned_by_org: Organization, permissions, description: str = ''):
    acl = AccessControlList.objects.create(name=name,
                                           description=description,
                                           owned_by_org=owned_by_org,
                                           default_acl=True,
                                           accessible_organization=owned_by_org)
    acl.permissions.add(*permissions)


@receiver(post_save, sender=Organization)
def handle_organization_creation(instance, created, **kwargs):
    """On organization creation, we create also one AccessControlList to allow administration of this Organization"""
    if created:
        organization = instance  # only for better reading

        admin_permissions, member_permissions = collect_default_permissions()

        create_acl(name=f"{organization.name} administrators",
                   description=_('Organization administrators can administrate all objects which are owned by the organization it self'),
                   owned_by_org=organization,
                   permissions=admin_permissions)
        create_acl(name=f"{organization.name} members",
                   description=_('Organization members can view all objects which are owned by the organization it self'),
                   owned_by_org=organization,
                   permissions=member_permissions)
