"""
Author: Michel Peltriaux
Organization: Spatial data infrastructure Rhineland-Palatinate, Germany
Contact: michel.peltriaux@vermkv.rlp.de
Created on: 06.05.19

"""
from getpass import getpass

from dateutil.parser import parse
from django.core.management import BaseCommand, call_command
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from MrMap.settings import MONITORING_REQUEST_TIMEOUT, MONITORING_TIME
from structure.models import MrMapGroup, Role, Permission, Organization, MrMapUser, Theme
from structure.settings import PUBLIC_ROLE_NAME, PUBLIC_GROUP_NAME, SUPERUSER_GROUP_NAME, SUPERUSER_ROLE_NAME
from monitoring.models import MonitoringSetting


class Command(BaseCommand):
    help = "Runs an initial setup for creating the superuser on a fresh installation."

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # first create themes
        self._create_themes()

        with transaction.atomic():
            # first run the main setup
            self._run_superuser_default_setup()
            # then load the default categories
            call_command('load_categories')

    def _create_themes(self):
        """ Adds default dark and light theme for frontend

        Returns:

        """
        Theme.objects.get_or_create(name='DARK')
        Theme.objects.get_or_create(name='LIGHT')

    def _run_superuser_default_setup(self):
        """ Encapsules the main setup for creating all default objects and the superuser

        Returns:
             nothing
        """
        # Check if superuser already exists
        name = input("Enter a username:")

        if MrMapUser.objects.filter(username=name).exists():
            self.stdout.write(self.style.NOTICE("User with that name already exists!"))
            return

        # check password
        password = getpass("Enter a password: ")
        password_conf = getpass("Enter the password again: ")
        while password != password_conf:
            self.stdout.write(self.style.ERROR("Passwords didn't match! Try again!"))
            password = getpass("Enter the password: ")
            password_conf = getpass("Enter the password again: ")

        superuser = MrMapUser.objects.create_superuser(
            name,
            "",
            password
        )
        superuser.confirmed_dsgvo = timezone.now()
        superuser.is_active = True
        superuser.theme = Theme.objects.get(name='LIGHT')
        superuser.save()
        msg = "Superuser '" + name + "' was created successfully!"
        self.stdout.write(self.style.SUCCESS(str(msg)))

        # handle default role
        self._create_default_role()

        # handle public group
        group = self._create_public_group(superuser)
        group.created_by = superuser
        group.user_set.add(superuser)
        group.save()

        # handle root group
        group = self._create_superuser_group(superuser)
        group.created_by = superuser
        group.user_set.add(superuser)
        group.save()


        # handle root organization
        orga = self._create_default_organization()
        superuser.organization = orga
        superuser.save()
        msg = "Superuser '" + name + "' added to group '" + group.name + "'!"
        self.stdout.write(self.style.SUCCESS(str(msg)))
        msg = "Superuser '" + name + "' added to organization '" + orga.organization_name + "'!"
        self.stdout.write(self.style.SUCCESS(msg))

        self._create_default_monitoring_setting()
        msg = (
            f"Default monitoring setting with check on {MONITORING_TIME} and "
            f"timeout {MONITORING_REQUEST_TIMEOUT} was created successfully"
        )
        self.stdout.write(self.style.SUCCESS(str(msg)))

    def _create_public_group(self, user: MrMapUser):
        """ Creates public group

        Args:
            user (MrMapUser): The superuser object
        Returns:
             group (Group): The newly created group
        """
        group = MrMapGroup.objects.get_or_create(
            name=PUBLIC_GROUP_NAME,
            created_by=user,
            is_public_group=True
        )[0]
        if group.role is None:
            role = Role.objects.get_or_create(name=PUBLIC_ROLE_NAME)[0]
            if role.permission is None:
                perm = Permission()
                for key, val in perm.__dict__.items():
                    if 'can_' in key:
                        setattr(perm, key, False)

                perm.save()
                role.permission = perm
            role.save()
            group.role = role
            group.created_by = user
        return group

    def _create_superuser_group(self, user: MrMapUser):
        """ Creates default group, default role for group and default superuser permission for role

        Args:
            user (MrMapUser): The superuser object
        Returns:
             group (Group): The newly created group
        """
        group = MrMapGroup.objects.get_or_create(name=SUPERUSER_GROUP_NAME, created_by=user)[0]
        if group.role is None:
            role = Role.objects.get_or_create(name=SUPERUSER_ROLE_NAME)[0]
            if role.permission is None:
                perm = Permission()
                for key, val in perm.__dict__.items():
                    if 'can_' in key:
                        setattr(perm, key, True)

                perm.save()
                role.permission = perm
            role.save()
            group.role = role
            group.created_by = user
        return group

    def _create_default_role(self):
        """ Create default role for average user -> has no permissions

        Returns:
             role (Role): The role which holds the permission
        """
        role = Role.objects.get_or_create(name="_default_")[0]
        if role.permission is None:
            perm = Permission()
            perm.save()
            role.permission = perm
            role.description = _("The default role for all groups. Has no permissions.")
        role.save()

    def _create_default_organization(self):
        """ Create default organization for superuser

        Returns:
            orga (Organization): The default organization
        """
        orga = Organization.objects.get_or_create(organization_name="Testorganization")[0]

        return orga

    def _create_default_monitoring_setting(self):
        """ Create default settings for monitoring

        Returns:
            nothing
        """
        mon_time = parse(MONITORING_TIME)
        monitoring_setting = MonitoringSetting.objects.get_or_create(
            check_time=mon_time, timeout=MONITORING_REQUEST_TIMEOUT
        )[0]
        monitoring_setting.save()
