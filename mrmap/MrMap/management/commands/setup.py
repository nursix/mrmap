"""
Author: Michel Peltriaux
Organization: Spatial data infrastructure Rhineland-Palatinate, Germany
Contact: michel.peltriaux@vermkv.rlp.de
Created on: 06.05.19

"""
import os
import random
import string

from dateutil.parser import parse
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand, call_command
from django.db import transaction, connections, DEFAULT_DB_ALIAS, OperationalError
from django.db.migrations.executor import MigrationExecutor
from django.utils import timezone

from monitoring.settings import MONITORING_REQUEST_TIMEOUT, MONITORING_TIME
from resourceNew.enums.service import OGCOperationEnum
from resourceNew.models.security import OGCOperation
from structure.models import Organization
from monitoring.models import MonitoringSetting


class Command(BaseCommand):
    help = "Runs an initial setup for creating the superuser on a fresh installation."

    def add_arguments(self, parser):
        parser.add_argument('--reset', dest='reset', action='store_true', help="calls reset_db command in front of setup routine.")
        parser.add_argument('--reset-force', dest='reset_force', action='store_true', help="calls reset_db command with --noinput arg in front of setup routine.")
        parser.add_argument('--collect-static', dest='collect_static', action='store_true', help="force to call collectstatic command.")

        parser.set_defaults(reset=False)
        parser.set_defaults(reset_force=False)
        parser.set_defaults(collect_static=False)

    def handle(self, *args, **options):
        if options['reset_force']:
            call_command('reset_db', '-c', '--noinput')
        elif options['reset']:
            call_command('reset_db', '-c')
        with transaction.atomic():
            self._pre_setup(**options)
            # sec run the main setup
            self._run_system_user_default_setup()
            self._run_superuser_default_setup()
            # then load the default categories
            call_command('load_categories')
            call_command('load_licences')
            # finally load the fixtures
            self._load_fixtures()

    @property
    def _super_user_exists(self):
        return get_user_model().objects.filter(username=os.environ.get("MRMAP_USER")).exists()

    def _is_database_synchronized(self, database):
        connection = connections[database]
        try:
            connection.prepare_database()
        except OperationalError:
            connection.connect()
            connection.prepare_database()
        executor = MigrationExecutor(connection)
        targets = executor.loader.graph.leaf_nodes()
        return not executor.migration_plan(targets)

    def _pre_setup(self, **options):
        """ check if there are pending migrations. If so, we migrate them"""
        if self._is_database_synchronized(DEFAULT_DB_ALIAS):
            # All migrations have been applied.
            pass
        else:
            call_command('migrate')

        if not self._super_user_exists or options['collect_static']:
            call_command("collectstatic", "--clear", "--noinput")
        #call_command('create_roles')

    def _run_system_user_default_setup(self):
        if get_user_model().objects.filter(username="system").exists():
            return
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for i in range(20))
        get_user_model().objects.create(username="system", password=password, is_active=False)

    def _run_superuser_default_setup(self):
        """ Encapsules the main setup for creating all default objects and the superuser

        Returns:
             nothing
        """
        if self._super_user_exists:
            return

        superuser = get_user_model().objects.create_superuser(
            username=os.environ.get("MRMAP_USER"),
            password=os.environ.get("MRMAP_PASSWORD")
        )
        superuser.confirmed_dsgvo = timezone.now()
        superuser.is_active = True
        superuser.save()
        msg = f"Superuser {os.environ.get('MRMAP_USER')} with password {os.environ.get('MRMAP_PASSWORD')} was created successfully!"
        self.stdout.write(self.style.SUCCESS(str(msg)))

        # handle root organization
        orga = self._create_default_organization()
        superuser.organization = orga
        superuser.save()
        msg = f"Superuser {os.environ.get('MRMAP_USER')} added to organization '" + str(orga.name) + "'!"
        self.stdout.write(self.style.SUCCESS(msg))

        self._create_default_monitoring_setting()
        msg = (
            f"Default monitoring setting with check on {MONITORING_TIME} and "
            f"timeout {MONITORING_REQUEST_TIMEOUT} was created successfully"
        )
        self.stdout.write(self.style.SUCCESS(str(msg)))

        self._create_ogc_operations()
        msg = "OgcOperations created"
        self.stdout.write((self.style.SUCCESS(msg)))

    @staticmethod
    def _create_default_organization():
        """ Create default organization for superuser

        Returns:
            orga (Organization): The default organization
        """
        orga = Organization.objects.get_or_create(name="Testorganization", is_autogenerated=False)[0]

        return orga

    @staticmethod
    def _create_default_monitoring_setting():
        """ Create default settings for monitoring

        Returns:
            nothing
        """
        mon_time = parse(MONITORING_TIME)
        monitoring_setting = MonitoringSetting.objects.get_or_create(
            check_time=mon_time, timeout=MONITORING_REQUEST_TIMEOUT
        )[0]
        monitoring_setting.save()

    @staticmethod
    def _create_ogc_operations():
        """ Create all possible OGCOperations in model ``OGCOperation´´

        Returns:
            nothing
        """
        for key, value in OGCOperationEnum.as_choices(drop_empty_choice=True):
            OGCOperation(operation=value).save()

    @staticmethod
    def _load_fixtures():
        # TODO: maybe develop a method to get a list of all available fixtures. Right now is not needed since only 5
        #  are available. It needs to be in the correct order, to avoid DB constraints.
        fixture_list = [
            "conformityCheckConfigurationInit.json",
            "conformityCheckConfigurationExternalInit.json",
            "ruleInit.json",
            "ruleSetInit.json",
            "conformityCheckConfigurationInternalInit.json"
        ]

        for index in range(len(fixture_list)):
            call_command('loaddata', fixture_list[index])
