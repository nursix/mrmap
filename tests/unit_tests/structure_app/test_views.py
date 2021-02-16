from copy import copy

from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from MrMap.messages import REQUEST_ACTIVATION_TIMEOVER, NO_PERMISSION, PUBLISH_PERMISSION_REMOVED, \
    PUBLISH_REQUEST_ACCEPTED, GROUP_INVITATION_EXISTS
from MrMap.settings import HTTP_OR_SSL, HOST_NAME
from structure.permissionEnums import PermissionEnum
from structure.models import Organization, PendingTask, MrMapGroup, Role, Permission, PublishRequest, \
    GroupInvitationRequest
from structure.tables import GroupTable, OrganizationTable, PublisherTable, PublisherRequestTable, PublishesForTable
from tests.baker_recipes.db_setup import create_superadminuser, create_non_autogenerated_orgas, create_guest_groups, \
    create_publish_request, create_pending_task, create_testuser
from tests.baker_recipes.structure_app.baker_recipes import PASSWORD


class StructureIndexViewTestCase(TestCase):

    def setUp(self):
        # creates user object in db
        self.user_password = PASSWORD
        self.groups = create_guest_groups(how_much_groups=9)
        self.user = create_superadminuser(groups=self.groups)
        self.orgas = create_non_autogenerated_orgas(user=self.user,
                                                    how_much_orgas=10)
        self.user.organization = self.orgas[0]
        self.user.save()
        self.user.refresh_from_db()
        self.pending_request = create_publish_request(
            group=self.groups[0],
            orga=self.user.organization,
            how_much_requests=10
        )

        self.pending_tasks = create_pending_task(group=self.groups[0], how_much_pending_tasks=10)

        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user_password)

    def test_get_index(self):
        response = self.client.get(
            reverse('structure:index', ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="views/structure_index.html")

        self.assertIsInstance(response.context['groups'], GroupTable)
        num_groups = self.user.get_groups().count()
        self.assertEqual(len(response.context['groups'].rows), num_groups)
        self.assertEqual(len(response.context['groups'].page.object_list), 5)

        self.assertIsInstance(response.context['organizations'], OrganizationTable)
        num_orgas = Organization.objects.all().count()
        self.assertEqual(len(response.context['organizations'].rows), num_orgas)
        self.assertEqual(len(response.context['organizations'].page.object_list), 5)

    def test_get_groups_index(self):
        response = self.client.get(
            reverse('structure:groups-index', ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="views/groups_index.html")

        self.assertIsInstance(response.context['groups'], GroupTable)
        num_groups = self.user.get_groups().count()
        self.assertEqual(len(response.context['groups'].rows), num_groups)
        self.assertEqual(len(response.context['groups'].page.object_list), 5)

    def test_get_organization_index(self):
        response = self.client.get(
            reverse('structure:organization_overview', ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="views/organizations_index.html")

        self.assertIsInstance(response.context['organizations'], OrganizationTable)
        num_orgas = Organization.objects.all().count()
        self.assertEqual(len(response.context['organizations'].rows), num_orgas)
        self.assertEqual(len(response.context['organizations'].page.object_list), 5)


class StructurePendingTaskViewTestCase(TestCase):
    def setUp(self):
        # creates user object in db
        self.user_password = PASSWORD
        self.groups = create_guest_groups(how_much_groups=9)
        self.user = create_superadminuser(groups=self.groups)
        self.orgas = create_non_autogenerated_orgas(user=self.user,
                                                    how_much_orgas=10)
        self.user.organization = self.orgas[0]
        self.user.save()
        self.user.refresh_from_db()
        self.pending_request = create_publish_request(
            group=self.groups[0],
            orga=self.user.organization,
            how_much_requests=10
        )

        self.pending_tasks = create_pending_task(group=self.groups[0], how_much_pending_tasks=10)

        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user_password)

    def test_remove_pending_task(self):
        response = self.client.get(
            reverse('structure:remove-task',
                    args=(self.pending_tasks[0].id,)),
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 303)
        self.assertEqual(PendingTask.objects.all().count(), 9)


class StructureDetailOrganizationViewTestCase(TestCase):
    def setUp(self):
        # creates user object in db
        self.user_password = PASSWORD
        self.groups = create_guest_groups(how_much_groups=9)
        self.user = create_superadminuser(groups=self.groups)
        self.orgas = create_non_autogenerated_orgas(user=self.user,
                                                    how_much_orgas=10)
        self.user.organization = self.orgas[0]
        self.user.save()
        self.user.refresh_from_db()
        self.pending_request = create_publish_request(
            group=self.groups[0],
            orga=self.user.organization,
            how_much_requests=10
        )

        self.pending_tasks = create_pending_task(group=self.groups[0], how_much_pending_tasks=10)

        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user_password)

    def test_get_detail_organization(self):
        response = self.client.get(
            reverse('structure:organization_details',
                    args=(self.orgas[0].id,)),
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response=response, template_name="views/organizations_detail.html")
        self.assertIsInstance(response.context['organization'], Organization)

        self.assertIsInstance(response.context['all_publisher_table'], PublisherTable)


class StructureEditOrganizationViewTestCase(TestCase):
    def setUp(self):
        # creates user object in db
        self.user_password = PASSWORD
        self.groups = create_guest_groups(how_much_groups=9)
        self.user = create_superadminuser(groups=self.groups)

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
            how_much_requests=10
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

        self.assertEqual(response.status_code, 302)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('You do not have permissions for this!', messages)

    def test_valid_edit_organization(self):
        perm = Permission.objects.get_or_create(name=PermissionEnum.CAN_EDIT_ORGANIZATION.value)[0]
        self.user.get_groups()[0].role.permissions.add(perm)

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
            reverse('structure:organization_edit',
                    args=(self.orgas[0].id,))+"?current-view=structure:index",
            data=params,
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )
        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.url, reverse('structure:index',))


class StructureRemoveOrganizationViewTestCase(TestCase):
    def setUp(self):
        # creates user object in db
        self.user_password = PASSWORD
        self.groups = create_guest_groups(how_much_groups=9)
        self.user = create_superadminuser(groups=self.groups)

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
            how_much_requests=10,
        )

        self.pending_tasks = create_pending_task(group=self.groups[0], how_much_pending_tasks=10)

        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user_password)

    def test_get_remove_organization(self):
        perm = Permission.objects.get_or_create(name=PermissionEnum.CAN_DELETE_ORGANIZATION.value)[0]
        self.user.get_groups()[0].role.permissions.add(perm)

        response = self.client.get(
            reverse('structure:organization_remove',
                    args=(self.orgas[0].id,))+"?current-view=structure:index",
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 200)

    def test_post_invalid_remove_organization(self):
        perm = Permission.objects.get_or_create(name=PermissionEnum.CAN_DELETE_ORGANIZATION.value)[0]
        self.user.get_groups()[0].role.permissions.add(perm)
        response2 = self.client.post(
            reverse('structure:organization_remove',
                    args=(self.orgas[0].id,))+"?current-view=structure:index",
            data={},
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response2.status_code, 422)

    def test_post_valid_remove_organization(self):
        perm = Permission.objects.get_or_create(name=PermissionEnum.CAN_DELETE_ORGANIZATION.value)[0]
        self.user.get_groups()[0].role.permissions.add(perm)

        org_name = self.orgas[0].organization_name

        response = self.client.post(
            reverse('structure:organization_remove',
                    args=(self.orgas[0].id,)),
            data={'is_confirmed': 'on', },
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 303)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('Organization {} successfully deleted.'.format(org_name), messages)

    def test_permission_remove_organization(self):
        response = self.client.get(
            reverse('structure:organization_remove',
                    args=(self.orgas[0].id,)),
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 302)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('You do not have permissions for this!', messages)


class StructureNewOrganizationViewTestCase(TestCase):
    def setUp(self):
        # creates user object in db
        self.user_password = PASSWORD
        self.groups = create_guest_groups(how_much_groups=9)
        self.user = create_superadminuser(groups=self.groups)

        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user_password)

    def test_get_new_organization(self):
        perm = Permission.objects.get_or_create(name=PermissionEnum.CAN_CREATE_ORGANIZATION.value)[0]
        self.user.get_groups()[0].role.permissions.add(perm)

        response = self.client.get(
            reverse('structure:organization_new', )+"?current-view=structure:index",
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 200)

    def test_post_valid_new_organization(self):
        perm = Permission.objects.get_or_create(name=PermissionEnum.CAN_CREATE_ORGANIZATION.value)[0]
        self.user.get_groups()[0].role.permissions.add(perm)

        post_params = {'organization_name': 'TestOrga', 'person_name': 'TestPerson'}

        response = self.client.post(
            reverse('structure:organization_new', )+"?current-view=structure:index",
            data=post_params,
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        latest = Organization.objects.latest('id')

        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.url, reverse('structure:index',))
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('Organization {} successfully created.'.format('TestOrga'), messages)

    def test_post_invalid_new_organization(self):
        perm = Permission.objects.get_or_create(name=PermissionEnum.CAN_CREATE_ORGANIZATION.value)[0]
        self.user.get_groups()[0].role.permissions.add(perm)

        post_params = {'person_name': 'TestPerson'}
        response = self.client.post(
            reverse('structure:organization_new')+"?current-view=structure:index",
            data=post_params,
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 422)

    def test_permission_new_organization(self):
        response = self.client.get(
            reverse('structure:organization_new'),
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 302)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('You do not have permissions for this!', messages)


class StructureDetailGroupViewTestCase(TestCase):
    def setUp(self):
        # creates user object in db
        self.user_password = PASSWORD
        self.groups = create_guest_groups(how_much_groups=9)
        self.user = create_superadminuser(groups=self.groups)
        self.orgas = create_non_autogenerated_orgas(user=self.user,
                                                    how_much_orgas=10)
        self.user.organization = self.orgas[0]
        self.user.save()
        self.user.refresh_from_db()
        self.pending_request = create_publish_request(
            group=self.groups[0],
            orga=self.user.organization,
            how_much_requests=10
        )

        self.pending_tasks = create_pending_task(group=self.groups[0], how_much_pending_tasks=10)

        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user_password)

    def test_get_detail_group(self):
        response = self.client.get(
            reverse('structure:group_details',
                    args=(self.groups[0].id,)),
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response=response, template_name="views/groups_detail.html")
        self.assertIsInstance(response.context['group'], MrMapGroup)

        self.assertIsInstance(response.context['all_publisher_table'], PublishesForTable)


class StructureNewGroupViewTestCase(TestCase):
    def setUp(self):
        # creates user object in db
        self.user_password = PASSWORD
        self.groups = create_guest_groups(how_much_groups=9)
        self.user = create_superadminuser(groups=self.groups)

        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user_password)

    def test_get_new_group(self):
        perm = Permission.objects.get_or_create(name=PermissionEnum.CAN_CREATE_GROUP.value)[0]
        self.user.get_groups()[0].role.permissions.add(perm)

        response = self.client.get(
            reverse('structure:new-group', )+"?current-view=structure:index",
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 200)

    def test_post_valid_new_group(self):
        perm = Permission.objects.get_or_create(name=PermissionEnum.CAN_CREATE_GROUP.value)[0]
        self.user.get_groups()[0].role.permissions.add(perm)

        post_params = {'name': 'TestGroup', 'role': Role.objects.latest('id').id}

        response = self.client.post(
            reverse('structure:new-group', )+"?current-view=structure:index",
            data=post_params,
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.url, reverse('structure:index',))
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('Group {} successfully created.'.format('TestGroup'), messages)

    def test_post_invalid_new_group(self):
        perm = Permission.objects.get_or_create(name=PermissionEnum.CAN_CREATE_GROUP.value)[0]
        self.user.get_groups()[0].role.permissions.add(perm)

        post_params = {}
        response = self.client.post(
            reverse('structure:new-group')+"?current-view=structure:index",
            data=post_params,
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 422)

    def test_permission_new_group(self):
        response = self.client.get(
            reverse('structure:new-group'),
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 302)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('You do not have permissions for this!', messages)


class StructureRemoveGroupViewTestCase(TestCase):
    def setUp(self):
        # creates user object in db
        self.user_password = PASSWORD
        self.groups = create_guest_groups(how_much_groups=9)
        self.user = create_superadminuser(groups=self.groups)

        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user_password)

    def test_get_remove_group(self):
        perm = Permission.objects.get_or_create(name=PermissionEnum.CAN_DELETE_GROUP.value)[0]
        self.user.get_groups()[0].role.permissions.add(perm)

        response = self.client.get(
            reverse('structure:delete-group',
                    args=(self.groups[0].id,))+"?current-view=structure:index",
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 200)

    def test_post_invalid_remove_group(self):
        perm = Permission.objects.get_or_create(name=PermissionEnum.CAN_DELETE_GROUP.value)[0]
        self.user.get_groups()[0].role.permissions.add(perm)

        response2 = self.client.post(
            reverse('structure:delete-group',
                    args=(self.groups[0].id,))+"?current-view=structure:index",
            data={},
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response2.status_code, 422)

    def test_post_valid_remove_group(self):
        perm = Permission.objects.get_or_create(name=PermissionEnum.CAN_DELETE_GROUP.value)[0]
        self.user.get_groups()[0].role.permissions.add(perm)

        first_group = self.groups[0]
        first_group.created_by = self.user
        first_group.name = "TestGroup"
        first_group.save()

        response = self.client.post(
            reverse('structure:delete-group',
                    args=(self.groups[0].id,)),
            data={'is_confirmed': 'on', },
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 303)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Group '{}' successfully deleted.".format("TestGroup"), messages)

    def test_permission_remove_group(self):
        response = self.client.get(
            reverse('structure:delete-group',
                    args=(self.groups[0].id,)),
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 302)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('You do not have permissions for this!', messages)


class StructureEditGroupViewTestCase(TestCase):
    def setUp(self):
        # creates user object in db
        self.user_password = PASSWORD
        self.groups = create_guest_groups(how_much_groups=9)
        self.user = create_superadminuser(groups=self.groups)

        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user_password)

    def test_permission_edit_group(self):
        response = self.client.get(
            reverse('structure:edit-group',
                    args=(self.groups[0].id,)),
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 302)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('You do not have permissions for this!', messages)

    def test_valid_edit_group(self):
        perm = Permission.objects.get_or_create(name=PermissionEnum.CAN_EDIT_GROUP.value)[0]
        self.user.get_groups()[0].role.permissions.add(perm)

        first_group = self.groups[0]
        first_group.created_by = self.user
        first_group.save()

        post_params = {'name': 'TestGroup', 'role': Role.objects.latest('id').id}

        response = self.client.post(
            reverse('structure:edit-group',
                    args=(self.groups[0].id,))+"?current-view=structure:index",
            data=post_params,
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.url, reverse('structure:index', ))


class StructureAcceptPublishRequestViewTestCase(TestCase):
    def setUp(self):
        # creates user object in db
        self.user_password = PASSWORD
        self.groups = create_guest_groups(how_much_groups=9)
        self.user = create_superadminuser(groups=self.groups)
        self.orgas = create_non_autogenerated_orgas(user=self.user,
                                                    how_much_orgas=10)
        self.user.organization = self.orgas[0]
        self.user.save()
        self.user.refresh_from_db()
        self.pending_request = create_publish_request(
            group=self.groups[0],
            orga=self.user.organization,
            message="Test",
            how_much_requests=10
        )

        for pending_request in self.pending_request:
            pending_request.activation_until = timezone.now() + timezone.timedelta(days=10)
            pending_request.save()

        self.pending_tasks = create_pending_task(group=self.groups[0], how_much_pending_tasks=10)

        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user_password)

    def test_permission_accept_publish_request(self):
        response = self.client.get(
            reverse('structure:toggle-publish-request',
                    args=(PublishRequest.objects.first().id,))
        )
        self.assertEqual(response.status_code, 302)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(NO_PERMISSION, messages)

    def test_valid_accept_publish_request(self):
        perm = Permission.objects.get_or_create(name=PermissionEnum.CAN_TOGGLE_PUBLISH_REQUESTS.value)[0]
        group = self.user.get_groups()[0]
        group.role.permissions.add(perm)

        post_params = {'accept': 'True', }
        pub_request = PublishRequest.objects.first()

        response = self.client.post(
            reverse('structure:toggle-publish-request',
                    args=(pub_request.id,)),
            data=post_params,
        )

        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(PUBLISH_REQUEST_ACCEPTED.format(pub_request.group.name), messages)
        self.assertEqual(response.status_code, 303)
        # Assert a redirect back to the dashboard, where the request can be handled
        self.assertEqual(response.url, reverse('home'))

    def test_invalid_accept_publish_request(self):
        perm = Permission.objects.get_or_create(name=PermissionEnum.CAN_TOGGLE_PUBLISH_REQUESTS.value)[0]
        self.user.get_groups()[0].role.permissions.add(perm)

        post_params = {'accept': "True", }

        public_request = PublishRequest.objects.first()
        public_request.activation_until = timezone.now() - timezone.timedelta(days=1)
        public_request.save()

        response = self.client.post(
            reverse('structure:toggle-publish-request',
                    args=(public_request.id,)),
            data=post_params,
        )

        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(REQUEST_ACTIVATION_TIMEOVER, messages)


class StructureRemovePublishRequestViewTestCase(TestCase):
    def setUp(self):
        # creates user object in db
        self.user_password = PASSWORD
        self.groups = create_guest_groups(how_much_groups=9)
        self.user = create_superadminuser(groups=self.groups)

        for group in self.groups:
            group.created_by = self.user
            group.save()

        self.orgas = create_non_autogenerated_orgas(user=self.user,
                                                    how_much_orgas=10)
        self.user.organization = self.orgas[0]
        self.user.save()
        self.user.refresh_from_db()

        self.user.get_groups()[0].publish_for_organizations.add(self.user.organization)

        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user_password)

    def test_permission_remove_publish_request(self):
        response = self.client.get(
            reverse('structure:remove-publisher',
                    args=(self.user.organization.id, self.user.get_groups()[0].id,)),
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 302)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('You do not have permissions for this!', messages)

    def test_valid_remove_publish_request(self):
        perm = Permission.objects.get_or_create(name=PermissionEnum.CAN_REMOVE_PUBLISHER.value)[0]
        group = self.user.get_groups()[0]
        group.role.permissions.add(perm)

        post_params = {'is_confirmed': 'on', }

        response = self.client.post(
            reverse('structure:remove-publisher',
                    args=(self.user.organization.id, group.id,)),
            data=post_params,
        )

        self.assertEqual(response.status_code, 303)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(PUBLISH_PERMISSION_REMOVED.format(group.name, self.user.organization.organization_name), messages)


class StructurePublishRequestViewTestCase(TestCase):
    def setUp(self):
        # creates user object in db
        self.user_password = PASSWORD
        self.groups = create_guest_groups(how_much_groups=9)
        self.user = create_superadminuser(groups=self.groups)
        self.orgas = create_non_autogenerated_orgas(user=self.user,
                                                    how_much_orgas=10)

        self.user.organization = self.orgas[0]
        self.user.organization.save()

        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user_password)

    def test_permission_publish_request_group(self):
        response = self.client.get(
            reverse('structure:publish-request',
                    args=(self.orgas[0].id,)),
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 302)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('You do not have permissions for this!', messages)

    def test_valid_publish_request(self):
        perm = Permission.objects.get_or_create(name=PermissionEnum.CAN_REQUEST_TO_BECOME_PUBLISHER.value)[0]
        self.user.get_groups()[0].role.permissions.add(perm)

        post_params = {'organization_name': 'TestOrganization',
                       'request_msg': 'test2',
                       'group': self.user.get_groups()[0].id}

        response = self.client.post(
            reverse('structure:publish-request',
                    args=(self.user.organization.id,)),
            data=post_params,
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )
        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.url, reverse('home'))


class StructureGroupInvitationRequestViewTestCase(TestCase):
    def setUp(self):
        # creates user object in db
        self.user_password = PASSWORD
        self.groups = create_guest_groups(how_much_groups=9)
        self.user = create_superadminuser(groups=self.groups)
        self.test_user = create_testuser()
        self.orgas = create_non_autogenerated_orgas(user=self.user,
                                                    how_much_orgas=10)

        self.user.organization = self.orgas[0]
        self.user.organization.save()

        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user_password)

    def test_create_group_invitation_not_logged_in(self):
        # User is not logged in
        client = copy(self.client)
        client.logout()
        url = str(reverse('structure:invite-user-to-group', args=(self.test_user.id,)))
        response = client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "{}?next={}".format(reverse("login"), url))

    def test_missing_permission_create_group_invitation(self):
        # User is missing permission
        response = self.client.get(
            reverse('structure:invite-user-to-group',
                    args=(self.test_user.id,)),
        )

        self.assertEqual(response.status_code, 302)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(NO_PERMISSION, messages)

    def test_call_group_invitation_form(self):
        # User has permission
        group = self.user.get_groups()[0]
        perm = Permission.objects.get_or_create(name=PermissionEnum.CAN_ADD_USER_TO_GROUP.value)[0]
        group.role.permissions.add(perm)

        response = self.client.get(
            reverse('structure:invite-user-to-group',
                    args=(self.test_user.id,)),
        )

        self.assertEqual(response.status_code, 200)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertNotIn(NO_PERMISSION, messages)

    def test_group_invitation_form_no_duplicates(self):
        # User has permission but can not create a second invitation to a user if there is already one!
        group = self.user.get_groups()[0]
        perm = Permission.objects.get_or_create(name=PermissionEnum.CAN_ADD_USER_TO_GROUP.value)[0]
        group.role.permissions.add(perm)

        params = {
            "message": "Test",
            "invited_user": self.test_user.id,
            "to_group": group.id,
        }

        response = self.client.post(
            reverse('structure:invite-user-to-group',
                    args=(self.test_user.id,)),
            data=params,
        )

        response = self.client.post(
            reverse('structure:invite-user-to-group',
                    args=(self.test_user.id,)),
            data=params,
        )

        # Expect a redirect back to the form
        self.assertEqual(response.status_code, 303)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        request = GroupInvitationRequest.objects.filter(
            created_by=self.user
        ).first()
        self.assertIn(GROUP_INVITATION_EXISTS.format(self.test_user, request.activation_until), messages)
