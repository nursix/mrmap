from datetime import date, timedelta

from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.urls import reverse
from MapSkinner.messages import ORGANIZATION_CAN_NOT_BE_OWN_PARENT, REQUEST_ACTIVATION_TIMEOVER
from MapSkinner.settings import HTTP_OR_SSL, HOST_NAME
from structure.forms import GroupForm, OrganizationForm, RemoveOrganizationForm, PublisherForOrganizationForm, \
    RemoveGroupForm
from structure.settings import PENDING_REQUEST_TYPE_PUBLISHING
from structure.models import Organization, PendingTask, MrMapGroup, Role
from structure.tables import GroupTable, OrganizationTable, PublisherTable, PublisherRequestTable, PublishesForTable
from tests.baker_recipes.db_setup import create_superadminuser, create_non_autogenerated_orgas, create_guest_groups, \
    create_pending_request, create_pending_task
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
        self.pending_request = create_pending_request(group=self.groups[0],
                                                      orga=self.user.organization,
                                                      type_str=PENDING_REQUEST_TYPE_PUBLISHING,
                                                      how_much_requests=10)

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
        self.assertEqual(len(response.context['groups'].rows), 10)
        self.assertEqual(len(response.context['groups'].page.object_list), 5)

        self.assertIsInstance(response.context['organizations'], OrganizationTable)
        self.assertEqual(len(response.context['organizations'].rows), 10)
        self.assertEqual(len(response.context['organizations'].page.object_list), 5)

        self.assertIsInstance(response.context['new_group_form'], GroupForm)
        self.assertIsInstance(response.context['new_organization_form'], OrganizationForm)

    def test_get_groups_index(self):
        response = self.client.get(
            reverse('structure:groups-index', ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="views/groups_index.html")

        self.assertIsInstance(response.context['groups'], GroupTable)
        self.assertEqual(len(response.context['groups'].rows), 10)
        self.assertEqual(len(response.context['groups'].page.object_list), 5)

        self.assertIsInstance(response.context['new_group_form'], GroupForm)

        # self.assertEqual(response.context['pub_requests_count'], 10)

    def test_get_organization_index(self):
        response = self.client.get(
            reverse('structure:organizations-index', ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="views/organizations_index.html")

        self.assertIsInstance(response.context['organizations'], OrganizationTable)
        self.assertEqual(len(response.context['organizations'].rows), 10)
        self.assertEqual(len(response.context['organizations'].page.object_list), 5)

        self.assertIsInstance(response.context['new_organization_form'], OrganizationForm)

        # self.assertEqual(response.context['pub_requests_count'], 10)


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
        self.pending_request = create_pending_request(group=self.groups[0],
                                                      orga=self.user.organization,
                                                      type_str=PENDING_REQUEST_TYPE_PUBLISHING,
                                                      how_much_requests=10)

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

        self.assertEqual(response.status_code, 302)
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
        self.pending_request = create_pending_request(group=self.groups[0],
                                                      orga=self.user.organization,
                                                      type_str=PENDING_REQUEST_TYPE_PUBLISHING,
                                                      how_much_requests=10)

        self.pending_tasks = create_pending_task(group=self.groups[0], how_much_pending_tasks=10)

        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user_password)

    def test_get_detail_organization(self):
        response = self.client.get(
            reverse('structure:detail-organization',
                    args=(self.orgas[0].id,)),
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response=response, template_name="views/organizations_detail.html")
        self.assertIsInstance(response.context['organization'], Organization)

        self.assertIsInstance(response.context['edit_organization_form'], OrganizationForm)
        self.assertIsInstance(response.context['delete_organization_form'], RemoveOrganizationForm)
        self.assertIsInstance(response.context['publisher_form'], PublisherForOrganizationForm)

        self.assertIsInstance(response.context['all_publisher_table'], PublisherTable)
        self.assertIsInstance(response.context['pub_requests_table'], PublisherRequestTable)
        self.assertEqual(len(response.context['pub_requests_table'].rows), 10)


class StructureEditOrganizationViewTestCase(TestCase):
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
        self.pending_request = create_pending_request(group=self.groups[0],
                                                      orga=self.user.organization,
                                                      type_str=PENDING_REQUEST_TYPE_PUBLISHING,
                                                      how_much_requests=10)

        self.pending_tasks = create_pending_task(group=self.groups[0], how_much_pending_tasks=10)

        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user_password)

    def test_permission_edit_organization(self):
        response = self.client.get(
            reverse('structure:edit-organization',
                    args=(self.orgas[0].id,)),
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 302)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('You do not have permissions for this!', messages)

    def test_valid_edit_organization(self):
        perm = self.user.get_groups()[0].role.permission
        perm.can_edit_organization = True
        perm.save()

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
            reverse('structure:edit-organization',
                    args=(self.orgas[0].id,)),
            data=params,
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.url, reverse('structure:detail-organization', args=(self.orgas[0].id,)))


class StructureRemoveOrganizationViewTestCase(TestCase):
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
        self.pending_request = create_pending_request(group=self.groups[0],
                                                      orga=self.user.organization,
                                                      type_str=PENDING_REQUEST_TYPE_PUBLISHING,
                                                      how_much_requests=10)

        self.pending_tasks = create_pending_task(group=self.groups[0], how_much_pending_tasks=10)

        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user_password)

    def test_get_remove_organization(self):
        perm = self.user.get_groups()[0].role.permission
        perm.can_delete_organization = True
        perm.save()

        response = self.client.get(
            reverse('structure:delete-organization',
                    args=(self.orgas[0].id,)),
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.url, reverse('structure:detail-organization', args=(self.orgas[0].id,)))

    def test_post_invalid_remove_organization(self):
        perm = self.user.get_groups()[0].role.permission
        perm.can_delete_organization = True
        perm.save()

        response2 = self.client.post(
            reverse('structure:delete-organization',
                    args=(self.orgas[0].id,)),
            data={},
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response2.status_code, 422)
        self.assertTrue(response2.context['show_delete_organization_form'])
        self.assertFormError(response2, 'delete_organization_form', 'is_confirmed', 'This field is required.')

    def test_post_valid_remove_organization(self):
        perm = self.user.get_groups()[0].role.permission
        perm.can_delete_organization = True
        perm.save()

        org_name = self.orgas[0].organization_name

        response = self.client.post(
            reverse('structure:delete-organization',
                    args=(self.orgas[0].id,)),
            data={'is_confirmed': 'on', },
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 303)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('Organization {} successfully deleted.'.format(org_name), messages)

    def test_permission_remove_organization(self):
        response = self.client.get(
            reverse('structure:delete-organization',
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
        perm = self.user.get_groups()[0].role.permission
        perm.can_create_organization = True
        perm.save()

        response = self.client.get(
            reverse('structure:new-organization', ),
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.url, reverse('structure:organizations-index'))

    def test_post_valid_new_organization(self):
        perm = self.user.get_groups()[0].role.permission
        perm.can_create_organization = True
        perm.save()

        post_params = {'organization_name': 'TestOrga', 'person_name': 'TestPerson'}

        response = self.client.post(
            reverse('structure:new-organization', ),
            data=post_params,
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        latest = Organization.objects.latest('id')

        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.url, reverse('structure:detail-organization', args=(latest.id,)))
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('Organization {} successfully created.'.format('TestOrga'), messages)

    def test_post_invalid_new_organization(self):
        perm = self.user.get_groups()[0].role.permission
        perm.can_create_organization = True
        perm.save()

        post_params = {'person_name': 'TestPerson'}
        response = self.client.post(
            reverse('structure:new-organization'),
            data=post_params,
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 422)
        self.assertTrue(response.context['show_new_organization_form'])
        self.assertFormError(response, 'new_organization_form', 'organization_name', 'This field is required.')

    def test_permission_new_organization(self):
        response = self.client.get(
            reverse('structure:new-organization'),
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
        self.pending_request = create_pending_request(group=self.groups[0],
                                                      orga=self.user.organization,
                                                      type_str=PENDING_REQUEST_TYPE_PUBLISHING,
                                                      how_much_requests=10)

        self.pending_tasks = create_pending_task(group=self.groups[0], how_much_pending_tasks=10)

        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user_password)

    def test_get_detail_group(self):
        response = self.client.get(
            reverse('structure:detail-group',
                    args=(self.groups[0].id,)),
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response=response, template_name="views/groups_detail.html")
        self.assertIsInstance(response.context['group'], MrMapGroup)

        self.assertIsInstance(response.context['edit_group_form'], GroupForm)
        self.assertIsInstance(response.context['delete_group_form'], RemoveGroupForm)
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
        perm = self.user.get_groups()[0].role.permission
        perm.can_create_group = True
        perm.save()

        response = self.client.get(
            reverse('structure:new-group', ),
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.url, reverse('structure:groups-index'))

    def test_post_valid_new_group(self):
        perm = self.user.get_groups()[0].role.permission
        perm.can_create_group = True
        perm.save()

        post_params = {'name': 'TestGroup', 'role': Role.objects.latest('id').id}

        response = self.client.post(
            reverse('structure:new-group', ),
            data=post_params,
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        latest = MrMapGroup.objects.latest('id')

        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.url, reverse('structure:detail-group', args=(latest.id,)))
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('Group {} successfully created.'.format('TestGroup'), messages)

    def test_post_invalid_new_group(self):
        perm = self.user.get_groups()[0].role.permission
        perm.can_create_group = True
        perm.save()

        post_params = {}
        response = self.client.post(
            reverse('structure:new-group'),
            data=post_params,
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 422)
        self.assertTrue(response.context['show_new_group_form'])
        self.assertFormError(response, 'new_group_form', 'name', 'This field is required.')

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
        perm = self.user.get_groups()[0].role.permission
        perm.can_delete_group = True
        perm.save()

        response = self.client.get(
            reverse('structure:delete-group',
                    args=(self.groups[0].id,)),
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.url, reverse('structure:detail-group', args=(self.groups[0].id,)))

    def test_post_invalid_remove_group(self):
        perm = self.user.get_groups()[0].role.permission
        perm.can_delete_group = True
        perm.save()

        response2 = self.client.post(
            reverse('structure:delete-group',
                    args=(self.groups[0].id,)),
            data={},
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response2.status_code, 422)
        self.assertTrue(response2.context['show_remove_group_form'])
        self.assertFormError(response2, 'remove_group_form', 'is_confirmed', 'This field is required.')

    def test_post_valid_remove_group(self):
        perm = self.user.get_groups()[0].role.permission
        perm.can_delete_group = True
        perm.save()

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
        perm = self.user.get_groups()[0].role.permission
        perm.can_edit_group = True
        perm.save()

        first_group = self.groups[0]
        first_group.created_by = self.user
        first_group.save()

        post_params = {'name': 'TestGroup', 'role': Role.objects.latest('id').id}

        response = self.client.post(
            reverse('structure:edit-group',
                    args=(self.groups[0].id,)),
            data=post_params,
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.url, reverse('structure:detail-group', args=(self.groups[0].id,)))


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
        self.pending_request = create_pending_request(group=self.groups[0],
                                                      orga=self.user.organization,
                                                      type_str=PENDING_REQUEST_TYPE_PUBLISHING,
                                                      how_much_requests=10)

        for pending_request in self.pending_request:
            pending_request.activation_until = date.today()
            pending_request.save()

        self.pending_tasks = create_pending_task(group=self.groups[0], how_much_pending_tasks=10)

        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user_password)

    def test_permission_accept_publish_request(self):
        response = self.client.get(
            reverse('structure:accept-publish-request',
                    args=(self.pending_request[0].id,)),
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 302)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('You do not have permissions for this!', messages)

    def test_valid_accept_publish_request(self):
        perm = self.user.get_groups()[0].role.permission
        perm.can_toggle_publish_requests = True
        perm.save()

        post_params = {'is_accepted': True, }

        response = self.client.post(
            reverse('structure:accept-publish-request',
                    args=(self.pending_request[0].id,)),
            post_params=post_params,
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.url, reverse('structure:detail-group', args=(self.groups[0].id,)))

    def test_invalid_accept_publish_request(self):
        perm = self.user.get_groups()[0].role.permission
        perm.can_toggle_publish_requests = True
        perm.save()

        post_params = {'is_accepted': True, }

        self.pending_request[0].activation_until = date.today() - timedelta(days=1)
        self.pending_request[0].save()

        response = self.client.post(
            reverse('structure:accept-publish-request',
                    args=(self.pending_request[0].id,)),
            post_params=post_params,
            HTTP_REFERER=HTTP_OR_SSL + HOST_NAME
        )

        self.assertEqual(response.status_code, 422)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(REQUEST_ACTIVATION_TIMEOVER, messages)
