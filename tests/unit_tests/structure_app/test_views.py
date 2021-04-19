from copy import copy

from django.contrib.auth.models import Permission
from django.contrib.messages import get_messages
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django_celery_results.models import TaskResult

from MrMap.messages import REQUEST_ACTIVATION_TIMEOVER, NO_PERMISSION, \
    PUBLISH_REQUEST_ACCEPTED, ORGANIZATION_SUCCESSFULLY_CREATED, \
    ORGANIZATION_SUCCESSFULLY_DELETED
from MrMap.settings import HTTP_OR_SSL, HOST_NAME
from structure.permissionEnums import PermissionEnum
<<<<<<< HEAD
from structure.models import Organization, PendingTask, PublishRequest
from structure.tables import OrganizationTable
from tests.baker_recipes.db_setup import create_non_autogenerated_orgas, \
=======
from structure.models import Organization, MrMapGroup, PublishRequest
from structure.tables import GroupTable, OrganizationTable
from tests.baker_recipes.db_setup import create_non_autogenerated_orgas, create_guest_groups, \
>>>>>>> 6547e7f6ad710c8351a3ede267a054c17a44fa14
    create_publish_request, create_pending_task, create_testuser
from tests.baker_recipes.structure_app.baker_recipes import PASSWORD


class StructureIndexViewTestCase(TestCase):

    def setUp(self):
        # creates user object in db
        self.user_password = PASSWORD
        self.user = create_testuser()
        self.orgas = create_non_autogenerated_orgas(user=self.user,
                                                    how_much_orgas=10)
        self.user.organization = self.orgas[0]
        self.user.save()
        self.user.refresh_from_db()
        self.pending_request = create_publish_request(
            group=self.groups[0],
            orga=self.user.organization,
        )

        self.pending_tasks = create_pending_task(group=self.groups[0], how_much_pending_tasks=10)

        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user_password)


    def test_get_organization_index(self):
        response = self.client.get(
            reverse('structure:organization_overview', ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="generic_views/generic_list.html")

        self.assertIsInstance(response.context['table'], OrganizationTable)
        num_orgas = Organization.objects.all().count()
        self.assertEqual(len(response.context['table'].rows), num_orgas)
        self.assertEqual(len(response.context['table'].page.object_list), 5)


class StructurePendingTaskViewTestCase(TestCase):
    def setUp(self):
        # creates user object in db
        self.user_password = PASSWORD
        self.groups = create_guest_groups(how_much_groups=9)
        self.user = create_testuser(groups=self.groups)
        self.orgas = create_non_autogenerated_orgas(user=self.user,
                                                    how_much_orgas=10)
        self.user.organization = self.orgas[0]
        self.user.save()
        self.user.refresh_from_db()
        self.pending_request = create_publish_request(
            group=self.groups[0],
            orga=self.user.organization,
        )

        self.pending_tasks = create_pending_task(group=self.groups[0], how_much_pending_tasks=10)

        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user_password)

    def test_remove_pending_task(self):
        response = self.client.post(
            reverse('structure:remove-task', args=[self.pending_tasks[0].pk]),
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 302)
<<<<<<< HEAD
        self.assertEqual(PendingTask.objects.count(), 9)
=======
>>>>>>> 6547e7f6ad710c8351a3ede267a054c17a44fa14


class StructureDetailOrganizationViewTestCase(TestCase):
    def setUp(self):
        # creates user object in db
        self.user_password = PASSWORD
        self.groups = create_guest_groups(how_much_groups=9)
        self.user = create_testuser(groups=self.groups)
        self.orgas = create_non_autogenerated_orgas(user=self.user,
                                                    how_much_orgas=10)
        self.user.organization = self.orgas[0]
        self.user.save()
        self.user.refresh_from_db()
        self.pending_request = create_publish_request(
            group=self.groups[0],
            orga=self.user.organization,
        )

        self.pending_tasks = create_pending_task(group=self.groups[0], how_much_pending_tasks=10)

        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user_password)

    def test_get_detail_organization(self):
        response = self.client.get(
            self.orgas[0].get_absolute_url(),
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response=response, template_name="MrMap/detail_views/table_tab.html")
        self.assertIsInstance(response.context['organization'], Organization)


class StructureEditOrganizationViewTestCase(TestCase):
    def setUp(self):
        # creates user object in db
        self.user_password = PASSWORD
        self.groups = create_guest_groups(how_much_groups=9)
        self.user = create_testuser(groups=self.groups)

        for group in self.groups:
            group.created_by = self.user
            group.save()

        self.orgas = create_non_autogenerated_orgas(user=self.user,
                                                    how_much_orgas=10)
        self.user.organization = self.orgas[0]
        self.user.save()
        self.user.refresh_from_db()
        self.pending_request = create_publish_request(
            group=self.groups[0],
            orga=self.user.organization,
        )

        self.pending_tasks = create_pending_task(group=self.groups[0], how_much_pending_tasks=10)

        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user_password)

    def test_permission_edit_organization(self):
        response = self.client.get(
            reverse('structure:organization_edit',
                    args=(self.orgas[0].id,)),
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 403)


    def test_valid_edit_organization(self):
        perm = Permission.objects.get(codename=PermissionEnum.CAN_EDIT_ORGANIZATION.value.split(".")[-1])
        self.user.groups.first().permissions.add(perm)

        params = {
            'organization_name': 'TestOrga',
            'description': 'This is a test',
            'parent': self.orgas[1].id,
            'person_name': 'Test name',
            'email': 'test@example.com',
            'phone': '+12 34567890',
            'facsimile': 'qwertz',
            'city': 'Musterstadt',
            'postal_code': '12345',
            'address': 'Musterweg 123',
            'state_or_province': 'RLP',
            'country': 'Germany',
        }

        response = self.client.post(
            reverse('structure:organization_edit', args=[self..orgas[0], ]),
            data=params,
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('structure:organization_view', args=[self.orgas[0], ]))


class StructureDetailGroupViewTestCase(TestCase):
    def setUp(self):
        # creates user object in db
        self.user_password = PASSWORD
        self.groups = create_guest_groups(how_much_groups=9)
        self.user = create_testuser(groups=self.groups)
        self.orgas = create_non_autogenerated_orgas(user=self.user,
                                                    how_much_orgas=10)
        self.user.organization = self.orgas[0]
        self.user.save()
        self.user.refresh_from_db()
        self.pending_request = create_publish_request(
            group=self.groups[0],
            orga=self.user.organization,
        )

        self.pending_tasks = create_pending_task(group=self.groups[0], how_much_pending_tasks=10)

        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user_password)


class StructureAcceptPublishRequestViewTestCase(TestCase):
    def setUp(self):
        # creates user object in db
        self.user_password = PASSWORD
        self.groups = create_guest_groups(how_much_groups=9)
        self.user = create_testuser(groups=self.groups)
        self.orgas = create_non_autogenerated_orgas(user=self.user,
                                                    how_much_orgas=10)
        self.user.organization = self.orgas[0]
        self.user.save()
        self.user.refresh_from_db()
        self.pending_request = create_publish_request(
            group=self.groups[0],
            orga=self.user.organization,
            message="Test",
        )

        self.pending_tasks = create_pending_task(group=self.groups[0], how_much_pending_tasks=10)

        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user_password)

    def test_permission_accept_publish_request(self):
        response = self.client.get(
            PublishRequest.objects.first().accept_request_uri
        )
        self.assertEqual(response.status_code, 403)

    def test_valid_accept_publish_request(self):
        perm = Permission.objects.get(codename=PermissionEnum.CAN_DELETE_PUBLISH_REQUEST.value.split(".")[-1])
        self.user.groups.first().permissions.add(perm)

        post_params = {'is_accepted': 'True', }
        pub_request = PublishRequest.objects.first()

        response = self.client.post(
            pub_request.accept_request_uri,
            data=post_params,
        )

        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(PUBLISH_REQUEST_ACCEPTED.format(pub_request.group.name), messages)
        self.assertEqual(response.status_code, 302)
        # Assert a redirect back to the dashboard, where the request can be handled
        self.assertEqual(response.url, reverse('structure:publish_request_overview'))

    def test_invalid_accept_publish_request(self):
        perm = Permission.objects.get(codename=PermissionEnum.CAN_DELETE_PUBLISH_REQUEST.value.split(".")[-1])
        self.user.groups.first().permissions.add(perm)

        post_params = {'is_accepted': "True", }

        public_request = PublishRequest.objects.first()
        public_request.delete()
        public_request = PublishRequest.objects.create(activation_until=timezone.now() - timezone.timedelta(days=1),
                                                       group=self.user.groups.select_related('mrmapgroup').first().mrmapgroup,
                                                       organization=self.user.organization,
                                                       message='test')

        response = self.client.post(
            public_request.accept_request_uri,
            data=post_params,
        )

        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(REQUEST_ACTIVATION_TIMEOVER, messages)


class StructureRemovePublishRequestViewTestCase(TestCase):
    def setUp(self):
        # creates user object in db
        self.user_password = PASSWORD
        self.groups = create_guest_groups(how_much_groups=9)
        self.user = create_testuser(groups=self.groups)

        for group in self.groups:
            group.created_by = self.user
            group.save()

        self.orgas = create_non_autogenerated_orgas(user=self.user,
                                                    how_much_orgas=10)
        self.user.organization = self.orgas[0]
        self.user.save()
        self.user.refresh_from_db()

        self.user.groups.all()[0].publish_for_organizations.add(self.user.organization)

        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user_password)


class StructurePublishRequestViewTestCase(TestCase):
    def setUp(self):
        # creates user object in db
        self.user_password = PASSWORD
        self.groups = create_guest_groups(how_much_groups=9)
        self.user = create_testuser(groups=self.groups)
        self.orgas = create_non_autogenerated_orgas(user=self.user,
                                                    how_much_orgas=10)

        self.user.organization = self.orgas[0]
        self.user.organization.save()

        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user_password)

    def test_valid_publish_request(self):
        perm = Permission.objects.get(codename=PermissionEnum.CAN_ADD_PUBLISH_REQUEST.value.split(".")[-1])
        self.user.groups.first().permissions.add(perm)

        post_params = {'organization': self.user.organization.id,
                       'request_msg': 'test2',
                       'group': self.user.groups.all()[0].id}

        response = self.client.post(
            reverse('structure:publish_request_new'),
            data=post_params,
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('structure:publish_request_overview')+f"?group={self.user.groups.all()[0].id}&organization={self.user.organization.id}")


class StructureGroupInvitationRequestViewTestCase(TestCase):
    def setUp(self):
        # creates user object in db
        self.user_password = PASSWORD
        self.groups = create_guest_groups(how_much_groups=9)
        self.user = create_testuser(groups=self.groups)
        self.orgas = create_non_autogenerated_orgas(user=self.user,
                                                    how_much_orgas=10)

        self.user.organization = self.orgas[0]
        self.user.organization.save()

        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user_password)

    def test_missing_permission_create_group_invitation(self):
        # User is missing permission
        response = self.client.get(
            reverse('structure:group_invitation_request_new'),
        )

        self.assertEqual(response.status_code, 403)

    def test_call_group_invitation_form(self):
        perm = Permission.objects.get(codename=PermissionEnum.CAN_ADD_USER_TO_GROUP.value.split(".")[-1])
        self.user.groups.first().permissions.add(perm)

        response = self.client.get(
            reverse('structure:group_invitation_request_new'),
        )

        self.assertEqual(response.status_code, 200)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertNotIn(NO_PERMISSION, messages)
