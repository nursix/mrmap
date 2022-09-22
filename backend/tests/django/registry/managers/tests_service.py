from pathlib import Path

from django.test import TestCase
from ows_lib.xml_mapper.utils import get_parsed_service
from registry.enums.service import HttpMethodEnum
from registry.models.service import (CatalougeService,
                                     CswOperationUrlQueryable,
                                     WebFeatureService, WebMapService)


class WebMapServiceCapabilitiesManagerTest(TestCase):

    def test_success(self):
        """Test that create manager function works correctly."""

        parsed_service = get_parsed_service(Path(Path.joinpath(
            Path(__file__).parent.resolve(), '../../test_data/capabilities/wms/1.3.0.xml')))

        WebMapService.capabilities.create(
            parsed_service=parsed_service)

        db_service = WebMapService.objects.count()
        self.assertEqual(1, db_service)


class WebFeatureServiceCapabilitiesManagerTest(TestCase):

    def test_success(self):
        """Test that create manager function works correctly."""

        parsed_service = get_parsed_service(Path(Path.joinpath(
            Path(__file__).parent.resolve(), '../../test_data/capabilities/wfs/2.0.0.xml')))

        WebFeatureService.capabilities.create(
            parsed_service=parsed_service)

        db_service = WebFeatureService.objects.count()
        self.assertEqual(1, db_service)


class CatalougeServiceCapabilitiesManagerTest(TestCase):

    def test_success(self):
        """Test that create_from_parsed_service manager function works correctly."""

        parsed_service = get_parsed_service(Path(Path.joinpath(
            Path(__file__).parent.resolve(), '../../test_data/csw_hessen_2_0_2.xml')))

        db_service = CatalougeService.capabilities.create_from_parsed_service(
            parsed_service=parsed_service)

        db_service_count = CatalougeService.objects.count()
        self.assertEqual(1, db_service_count)

        queryables = CswOperationUrlQueryable.objects.closest_matches(
            value="Type", operation="GetRecords", service_id=db_service.pk).filter(operation_url__method=HttpMethodEnum.GET.value)

        self.assertEqual(2, queryables.count())
