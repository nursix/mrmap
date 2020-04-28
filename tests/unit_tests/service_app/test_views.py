import logging

from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.urls import reverse
from MapSkinner.consts import SERVICE_ADD
from MapSkinner.messages import SERVICE_ACTIVATED, SERVICE_DEACTIVATED, SERVICE_UPDATE_WRONG_TYPE
from service.forms import RegisterNewServiceWizardPage1, RegisterNewServiceWizardPage2, RemoveServiceForm, \
    UpdateOldToNewElementsForm
from service.helper.enums import OGCServiceEnum
from service.models import Layer, FeatureType, Service, Metadata
from service.tables import WmsServiceTable, WfsServiceTable, PendingTasksTable
from structure.models import PendingTask, GroupActivity
from tests.baker_recipes.db_setup import *
from tests.baker_recipes.structure_app.baker_recipes import PASSWORD
from tests.test_data import get_capabilitites_url


class ServiceIndexViewTestCase(TestCase):
    def setUp(self):
        self.logger = logging.getLogger('ServiceViewTestCase')
        self.user = create_superadminuser()
        self.client = Client()
        self.client.login(username=self.user.username, password=PASSWORD)
        self.wms_services = create_wms_service(group=self.user.get_groups().first(), how_much_services=10)
        self.wfs_services = create_wfs_service(group=self.user.get_groups().first(), how_much_services=10)
        create_wms_service(is_update_candidate_for=self.wms_services[0].service, user=self.user,
                           group=self.user.get_groups().first())
        create_wfs_service(is_update_candidate_for=self.wfs_services[0].service, user=self.user,
                           group=self.user.get_groups().first())

    def test_get_index_view(self):
        response = self.client.get(
            reverse('service:index', ),
        )
        self.assertEqual(response.status_code, 200, )
        self.assertTemplateUsed(response=response, template_name="views/index.html")
        self.assertIsInstance(response.context["wms_table"], WmsServiceTable)
        self.assertEqual(len(response.context["wms_table"].rows), 10)
        # see if paging is working... only 5 elements by default should be listed
        self.assertEqual(len(response.context["wms_table"].page.object_list), 5)

        self.assertIsInstance(response.context["wfs_table"], WfsServiceTable)
        self.assertEqual(len(response.context["wfs_table"].rows), 10)
        # see if paging is working... only 5 elements by default should be listed
        self.assertEqual(len(response.context["wfs_table"].page.object_list), 5)

        self.assertIsInstance(response.context["pt_table"], PendingTasksTable)
        self.assertIsInstance(response.context["new_service_form"], RegisterNewServiceWizardPage1)
        self.assertEqual(reverse(SERVICE_ADD,), response.context["new_service_form"].action_url)


class ServiceWmsIndexViewTestCase(TestCase):
    def setUp(self):
        self.logger = logging.getLogger('ServiceViewTestCase')
        self.user = create_superadminuser()
        self.client = Client()
        self.client.login(username=self.user.username, password=PASSWORD)
        create_wms_service(group=self.user.get_groups().first(), how_much_services=10)

    def test_get_index_view(self):
        response = self.client.get(
            reverse('service:wms-index', ),
        )
        self.assertEqual(response.status_code, 200, )
        self.assertTemplateUsed(response=response, template_name="views/wms_index.html")
        self.assertIsInstance(response.context["wms_table"], WmsServiceTable)
        self.assertEqual(len(response.context["wms_table"].rows), 10)
        # see if paging is working... only 5 elements by default should be listed
        self.assertEqual(len(response.context["wms_table"].page.object_list), 5)

        self.assertIsInstance(response.context["pt_table"], PendingTasksTable)
        self.assertIsInstance(response.context["new_service_form"], RegisterNewServiceWizardPage1)
        self.assertEqual(reverse(SERVICE_ADD,), response.context["new_service_form"].action_url)


class ServiceWfsIndexViewTestCase(TestCase):
    def setUp(self):
        self.logger = logging.getLogger('ServiceViewTestCase')
        self.user = create_superadminuser()
        self.client = Client()
        self.client.login(username=self.user.username, password=PASSWORD)
        create_wms_service(group=self.user.get_groups().first(), how_much_services=10)
        create_wfs_service(group=self.user.get_groups().first(), how_much_services=10)

    def test_get_index_view(self):
        response = self.client.get(
            reverse('service:wfs-index', ),
        )
        self.assertEqual(response.status_code, 200, )
        self.assertTemplateUsed(response=response, template_name="views/wfs_index.html")
        self.assertIsInstance(response.context["wfs_table"], WfsServiceTable)
        self.assertEqual(len(response.context["wfs_table"].rows), 10)
        # see if paging is working... only 5 elements by default should be listed
        self.assertEqual(len(response.context["wfs_table"].page.object_list), 5)

        self.assertIsInstance(response.context["pt_table"], PendingTasksTable)
        self.assertIsInstance(response.context["new_service_form"], RegisterNewServiceWizardPage1)
        self.assertEqual(reverse(SERVICE_ADD,), response.context["new_service_form"].action_url)


class ServiceAddViewTestCase(TestCase):

    def setUp(self):
        self.logger = logging.getLogger('ServiceAddViewTestCase')
        self.user = create_superadminuser()
        self.client = Client()
        self.client.login(username=self.user.username, password=PASSWORD)

    def test_redirect_if_http_get(self):
        response = self.client.get(reverse('service:add'))
        self.assertEqual(response.status_code, 303, msg="No redirect was done")
        self.assertEqual(response.url, reverse('service:index'), msg="Redirect wrong")

    def test_permission_denied_page1(self):
        post_params = {
            'page': '1',
            'get_request_uri': get_capabilitites_url().get('valid')
        }

        # remove permission to add new services
        perm = self.user.get_groups()[0].role.permission
        perm.can_register_service = False
        perm.save()

        response = self.client.post(reverse('service:add'), HTTP_REFERER=reverse('service:add'), data=post_params,)
        self.assertEqual(response.status_code, 302)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('You do not have permissions for this!', messages)

    def test_post_new_service_wizard_page1_valid_input(self):
        post_params={
            'page': '1',
            'get_request_uri': get_capabilitites_url().get('valid')
        }

        response = self.client.post(reverse('service:add'), data=post_params)

        self.assertEqual(response.status_code, 202,)
        self.assertIsInstance(response.context['new_service_form'], RegisterNewServiceWizardPage2)

    def test_post_new_service_wizard_page1_invalid_version(self):
        post_params = {
            'page': '1',
            'get_request_uri': get_capabilitites_url().get('invalid_version')
        }

        response = self.client.post(reverse('service:add'), data=post_params)

        self.assertEqual(response.status_code, 422, )
        self.assertIsInstance(response.context['new_service_form'], RegisterNewServiceWizardPage1)
        self.assertFormError(response, 'new_service_form', 'get_request_uri', 'The given {} version {} is not supported from Mr. Map.'.format(OGCServiceEnum.WMS.value, '9.4.0'))

    def test_post_new_service_wizard_page1_invalid_no_service(self):
        post_params = {
            'page': '1',
            'get_request_uri': get_capabilitites_url().get('invalid_no_service')
        }

        response = self.client.post(reverse('service:add'), data=post_params)

        self.assertEqual(response.status_code, 422, )
        self.assertIsInstance(response.context['new_service_form'], RegisterNewServiceWizardPage1)
        self.assertFormError(response, 'new_service_form', 'get_request_uri', 'The given uri is not valid cause there is no service parameter.')

    def test_post_new_service_wizard_page1_invalid_no_version(self):
        post_params = {
            'page': '1',
            'get_request_uri': get_capabilitites_url().get('invalid_no_version')
        }

        response = self.client.post(reverse('service:add'), data=post_params)

        self.assertEqual(response.status_code, 422, )
        self.assertIsInstance(response.context['new_service_form'], RegisterNewServiceWizardPage1)
        self.assertFormError(response, 'new_service_form', 'get_request_uri', 'The given uri is not valid cause there is no version parameter.')

    def test_post_new_service_wizard_page1_invalid_no_request(self):
        post_params = {
            'page': '1',
            'get_request_uri': get_capabilitites_url().get('invalid_no_request')
        }

        response = self.client.post(reverse('service:add'), data=post_params)

        self.assertEqual(response.status_code, 422, )
        self.assertIsInstance(response.context['new_service_form'], RegisterNewServiceWizardPage1)
        self.assertFormError(response, 'new_service_form', 'get_request_uri', 'The given uri is not valid cause there is no request parameter.')

    def test_post_new_service_wizard_page1_invalid_servicetype(self):
        post_params = {
            'page': '1',
            'get_request_uri': get_capabilitites_url().get('invalid_servicetype')
        }

        response = self.client.post(reverse('service:add'), data=post_params)

        self.assertEqual(response.status_code, 422, )
        self.assertIsInstance(response.context['new_service_form'], RegisterNewServiceWizardPage1)
        self.assertFormError(response, 'new_service_form', 'get_request_uri', 'The given service typ is not supported from Mr. Map.')

    def test_post_new_service_wizard_page2(self):
        post_params = {
            'page': '2',
            'is_form_update': 'False',
            'ogc_request': 'GetCapabilities',
            'ogc_service': 'wms',
            'ogc_version': '1.3.0',
            'uri': 'http://geo5.service24.rlp.de/wms/karte_rp.fcgi?',
            'registering_with_group': self.user.get_groups()[0].id,
        }

        response = self.client.post(reverse('service:add'), data=post_params)
        self.assertEqual(response.status_code, 303, )
        self.assertEqual(response.url, reverse('service:index'), msg="Redirect wrong")
        self.assertEqual(PendingTask.objects.all().count(), 1)

    def test_post_update_new_service_wizard_page2(self):
        post_params = {
            'page': '2',
            'is_form_update': 'True',
            'ogc_request': 'GetCapabilities',
            'ogc_service': 'wms',
            'ogc_version': '1.3.0',
            'uri': 'http://geo5.service24.rlp.de/wms/karte_rp.fcgi?',
            'registering_with_group': self.user.get_groups()[0].id,
        }

        response = self.client.post(reverse('service:add'), data=post_params)
        self.assertEqual(response.status_code, 200, )
        self.assertFalse(response.context['new_service_form'].fields['is_form_update'].initial)


class ServiceRemoveViewTestCase(TestCase):

    def setUp(self):
        self.logger = logging.getLogger('ServiceAddViewTestCase')
        self.user = create_superadminuser()
        self.client = Client()
        self.client.login(username=self.user.username, password=PASSWORD)
        self.wms_service_metadatas = create_wms_service(self.user.get_groups().first(), 1)
        self.wfs_service_metadatas = create_wfs_service(self.user.get_groups().first(), 1)

    def test_remove_wms_service(self):
        post_data = {
            'is_confirmed': 'on'
        }
        metadata = self.wms_service_metadatas[0]
        response = self.client.post(reverse('service:remove', args=[metadata.id]), data=post_data)
        self.assertEqual(response.status_code, 303)

        metadata.refresh_from_db()
        self.assertTrue(metadata.is_deleted, msg="Metadata is not marked as deleted.")

        sub_elements = Layer.objects.filter(parent_service__metadata=metadata)
        for sub_element in sub_elements:
            sub_metadata = sub_element.metadata
            self.assertTrue(sub_metadata.is_deleted, msg="Metadata of subelement is not marked as deleted.")

        self.assertEqual(GroupActivity.objects.all().count(), 1)

    def test_remove_wfs_service(self):
        post_data = {
            'is_confirmed': 'on'
        }
        metadata = self.wfs_service_metadatas[0]
        response = self.client.post(reverse('service:remove', args=[self.wfs_service_metadatas[0].id]), data=post_data)
        self.assertEqual(response.status_code, 303)

        metadata.refresh_from_db()
        self.assertTrue(metadata.is_deleted, msg="Metadata is not marked as deleted.")

        sub_elements = FeatureType.objects.filter(parent_service__metadata=metadata)
        for sub_element in sub_elements:
            sub_metadata = sub_element.metadata
            self.assertTrue(sub_metadata.is_deleted, msg="Metadata of subelement is not marked as deleted.")

        self.assertEqual(GroupActivity.objects.all().count(), 1)

    def test_remove_service_invalid_form(self):

        response = self.client.post(reverse('service:remove', args=[self.wms_service_metadatas[0].id]),)
        self.assertEqual(response.status_code, 422)
        self.assertFalse(response.context['remove_service_form'].is_valid())

    def test_permission_denied_remove(self):

        # remove permission to remove services
        perm = self.user.get_groups()[0].role.permission
        perm.can_remove_service = False
        perm.save()

        response = self.client.post(reverse('service:remove',
                                    args=[self.wms_service_metadatas[0].id]),
                                    HTTP_REFERER=reverse('service:remove', args=[self.wms_service_metadatas[0].id]),)
        self.assertEqual(response.status_code, 302)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('You do not have permissions for this!', messages)


class ServiceActivateViewTestCase(TestCase):

    def setUp(self):
        self.logger = logging.getLogger('ServiceAddViewTestCase')
        self.user = create_superadminuser()
        self.client = Client()
        self.client.login(username=self.user.username, password=PASSWORD)
        self.wms_service_metadatas = create_wms_service(self.user.get_groups().first(), 1)

    def test_activate_service(self):

        service = self.wms_service_metadatas[0].service
        response = self.client.post(reverse('service:activate', args=[service.id]),)
        self.assertEqual(response.status_code, 303)
        messages = [m.message for m in get_messages(response.wsgi_request)]

        activated_status = service.metadata.is_active
        if activated_status:
            self.assertIn(SERVICE_DEACTIVATED.format(self.wms_service_metadatas[0].title), messages)
        else:
            self.assertIn(SERVICE_ACTIVATED.format(self.wms_service_metadatas[0].title), messages)

    def test_permission_denied_activate_service(self):
        # remove permission to remove services
        perm = self.user.get_groups()[0].role.permission
        perm.can_activate_service = False
        perm.save()

        service = self.wms_service_metadatas[0].service
        response = self.client.post(reverse('service:activate',
                                            args=[service.id]),
                                    HTTP_REFERER=reverse('service:activate', args=[service.id]), )
        self.assertEqual(response.status_code, 302)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('You do not have permissions for this!', messages)


class ServiceDetailViewTestCase(TestCase):

    def setUp(self):
        self.logger = logging.getLogger('ServiceAddViewTestCase')
        self.user = create_superadminuser()
        self.client = Client()
        self.client.login(username=self.user.username, password=PASSWORD)
        self.wms_service_metadatas = create_wms_service(self.user.get_groups().first(), 1)
        self.wfs_service_metadatas = create_wfs_service(self.user.get_groups().first(), 1)

    def test_get_detail_wms(self):
        response = self.client.get(reverse('service:detail', args=[self.wms_service_metadatas[0].id]), )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="views/detail.html")

    def test_get_detail_wms_sublayer(self):
        service = self.wms_service_metadatas[0].service
        sublayer_services = Service.objects.filter(
            parent_service=service
        )
        response = self.client.get(reverse('service:detail', args=[sublayer_services[0].metadata.id]), )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="views/sublayer_detail.html")

    def test_get_detail_wms_sublayer_without_base_extending(self):
        service = self.wms_service_metadatas[0].service
        sublayer_services = Service.objects.filter(
            parent_service=service
        )
        response = self.client.get(reverse('service:detail', args=[sublayer_services[0].metadata.id]) + '?no-base', )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="views/sublayer_detail_no_base.html")

    def test_get_detail_wfs(self):
        response = self.client.post(reverse('service:detail', args=[self.wfs_service_metadatas[0].id]), )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="views/detail.html")

    def test_get_detail_wfs_featuretype(self):
        service = self.wfs_service_metadatas[0].service
        featuretypes = FeatureType.objects.filter(
            parent_service=service
        )
        response = self.client.get(reverse('service:detail', args=[featuretypes[0].metadata.id]), )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="views/featuretype_detail.html")

    def test_get_detail_wfs_featuretype_without_base_extending(self):
        service = self.wfs_service_metadatas[0].service
        featuretypes = FeatureType.objects.filter(
            parent_service=service
        )
        response = self.client.get(reverse('service:detail', args=[featuretypes[0].metadata.id]) + '?no-base', )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="views/featuretype_detail_no_base.html")

    def test_get_detail_404(self):
        response = self.client.post(reverse('service:detail', args=[9999]), )
        self.assertEqual(response.status_code, 404)

    def test_get_detail_context(self):
        response = self.client.get(reverse('service:detail', args=[self.wms_service_metadatas[0].id]), )
        self.assertIsInstance(response.context['remove_service_form'], RemoveServiceForm)
        self.assertEqual(response.context['remove_service_form'].action_url, reverse('service:remove', args=[self.wms_service_metadatas[0].id]))
        self.assertIsInstance(response.context['service_md'], Metadata)


class ServicePendingTaskViewTestCase(TestCase):
    def setUp(self):
        self.user = create_superadminuser()
        self.client = Client()
        self.client.login(username=self.user.username, password=PASSWORD)
        create_pending_task(self.user.get_groups().first(), 10)

    def test_get_pending_tasks_view(self):
        response = self.client.get(
            reverse('service:pending-tasks', ),
        )
        self.assertEqual(response.status_code, 200, )
        self.assertTemplateUsed(response=response, template_name="includes/pending_tasks.html")
        self.assertIsInstance(response.context["pt_table"], PendingTasksTable)
        self.assertEqual(len(response.context["pt_table"].rows), 10)


class NewUpdateServiceViewTestCase(TestCase):
    def setUp(self):
        self.user = create_superadminuser()
        self.client = Client()
        self.client.login(username=self.user.username, password=PASSWORD)

        self.wms_metadatas = create_wms_service(self.user.get_groups().first(), 1)

    def test_get_update_service_view(self):
        response = self.client.get(
            reverse('service:new-pending-update', args=(self.wms_metadatas[0].id,)),
        )
        self.assertEqual(response.status_code, 303)

    def test_post_valid_update_service_page1(self):
        params = {
            'page': '1',
            'get_capabilities_uri': get_capabilitites_url().get('valid'),
        }
        response = self.client.post(
            reverse('service:new-pending-update', args=(self.wms_metadatas[0].id,)),
            data=params
        )
        self.assertEqual(response.status_code, 303)
        try:
            Service.objects.get(is_update_candidate_for=self.wms_metadatas[0].service.id)
        except ObjectDoesNotExist:
            self.fail("No update candidate were found for the service.")

    def test_post_invalid_no_service_update_service_page1(self):
        params = {
            'page': '1',
            'get_capabilities_uri': get_capabilitites_url().get('invalid_no_service'),
        }

        response = self.client.post(
            reverse('service:new-pending-update', args=(self.wms_metadatas[0].id,)),
            data=params
        )

        self.assertEqual(response.status_code, 422)
        self.assertTrue(response.context['show_update_form'])
        self.assertFormError(response, 'update_service_form', 'get_capabilities_uri', 'The given uri is not valid cause there is no service parameter.')

    def test_post_invalid_servicetype_update_service_page1(self):
        params = {
            'page': '1',
            'get_capabilities_uri': get_capabilitites_url().get('valid_wfs_version_202'),
        }

        response = self.client.post(
            reverse('service:new-pending-update', args=(self.wms_metadatas[0].id,)),
            data=params
        )

        self.assertEqual(response.status_code, 422)
        self.assertTrue(response.context['show_update_form'])
        self.assertFormError(response, 'update_service_form', None, SERVICE_UPDATE_WRONG_TYPE)

    def test_post_invalid_update_candidate_exists_update_service_page1(self):
        params = {
            'page': '1',
            'get_capabilities_uri': get_capabilitites_url().get('valid'),
        }
        create_wms_service(is_update_candidate_for=self.wms_metadatas[0].service, group=self.user.get_groups()[0], user=self.user)

        response = self.client.post(
            reverse('service:new-pending-update', args=(self.wms_metadatas[0].id,)),
            data=params
        )
        self.assertEqual(response.status_code, 422)
        self.assertFormError(response, 'update_service_form', None, "There are still pending update requests from user '{}' for this service.".format(self.user))


class PendingUpdateServiceViewTestCase(TestCase):
    def setUp(self):
        self.user = create_superadminuser()
        self.client = Client()
        self.client.login(username=self.user.username, password=PASSWORD)

        self.wms_metadata = create_wms_service(self.user.get_groups().first(), 1)[0]
        self.wms_update_candidate = create_wms_service(is_update_candidate_for=self.wms_metadata.service, group=self.user.get_groups()[0], user=self.user)

        self.wfs_metadata = create_wfs_service(self.user.get_groups().first(), 1)[0]
        self.wfs_update_candidate = create_wfs_service(is_update_candidate_for=self.wfs_metadata.service, group=self.user.get_groups()[0], user=self.user)

    def test_get_pending_update_wms_service_view(self):
        response = self.client.get(
            reverse('service:pending-update', args=(self.wms_metadata.id,)),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response=response, template_name="views/service_update.html")
        self.assertIsInstance(response.context["current_service"], Service)
        self.assertIsInstance(response.context["update_service"], Service)
        self.assertIsInstance(response.context["diff_elements"], dict)
        self.assertIsInstance(response.context["update_confirmation_form"], UpdateOldToNewElementsForm)

    def test_get_pending_update_wfs_service_view(self):
        response = self.client.get(
            reverse('service:pending-update', args=(self.wfs_metadata.id,)),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response=response, template_name="views/service_update.html")
        self.assertIsInstance(response.context["current_service"], Service)
        self.assertIsInstance(response.context["update_service"], Service)
        self.assertIsInstance(response.context["diff_elements"], dict)
        self.assertIsInstance(response.context["update_confirmation_form"], UpdateOldToNewElementsForm)


class DismissPendingUpdateServiceViewTestCase(TestCase):
    def setUp(self):
        self.user = create_superadminuser()
        self.client = Client()
        self.client.login(username=self.user.username, password=PASSWORD)

        self.wms_metadata = create_wms_service(self.user.get_groups().first(), 1)[0]
        self.wms_update_candidate = create_wms_service(is_update_candidate_for=self.wms_metadata.service, group=self.user.get_groups()[0], user=self.user)

        self.wfs_metadata = create_wfs_service(self.user.get_groups().first(), 1)[0]
        self.wfs_update_candidate = create_wfs_service(is_update_candidate_for=self.wfs_metadata.service, group=self.user.get_groups()[0], user=self.user)

    def test_get_dismiss_pending_update_wms_service_view(self):
        response = self.client.get(
            reverse('service:dismiss-pending-update', args=(self.wms_metadata.id,)),
        )
        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.url, reverse('service:pending-update', args=(self.wms_metadata.id,)))

    def test_get_dismiss_pending_update_wfs_service_view(self):
        response = self.client.get(
            reverse('service:dismiss-pending-update', args=(self.wfs_metadata.id,)),
        )
        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.url, reverse('service:pending-update', args=(self.wfs_metadata.id,)))

    def test_post_dismiss_pending_update_wms_service_view(self):
        response = self.client.post(
            reverse('service:dismiss-pending-update', args=(self.wms_metadata.id,)),
        )
        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.url, reverse('service:detail', args=(self.wms_metadata.id,)))

    def test_post_dismiss_pending_update_wfs_service_view(self):
        response = self.client.post(
            reverse('service:dismiss-pending-update', args=(self.wfs_metadata.id,)),
        )
        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.url, reverse('service:detail', args=(self.wfs_metadata.id,)))
