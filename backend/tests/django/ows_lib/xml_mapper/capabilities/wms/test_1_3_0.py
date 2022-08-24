import os

from django.contrib.gis.geos import Polygon
from django.test import SimpleTestCase
from eulxml.xmlmap import load_xmlobject_from_file
from isodate.isodatetime import parse_datetime
from isodate.isoduration import parse_duration
from ows_lib.xml_mapper.capabilities.mixins import OperationUrl
from ows_lib.xml_mapper.capabilities.wms.mixins import TimeExtent
from ows_lib.xml_mapper.capabilities.wms.wms130 import Layer, WebMapService
from ows_lib.xml_mapper.namespaces import WMS_1_3_0_NAMESPACE, XLINK_NAMESPACE
from tests.django.settings import DJANGO_TEST_ROOT_DIR


class WebMapServiceTestCase(SimpleTestCase):

    def setUp(self) -> None:
        path = os.path.join(DJANGO_TEST_ROOT_DIR,
                            "./test_data/capabilities/wms/1.3.0.xml")

        self.parsed_capabilities: WebMapService = load_xmlobject_from_file(
            path, xmlclass=WebMapService)

    def _test_root_mapper(self):
        self.assertEqual(self.parsed_capabilities.service_url,
                         "https://maps.dwd.de/geoserver/")

    def _test_service_metadata_mapper(self):
        self.assertEqual(
            self.parsed_capabilities.service_metadata.title,
            "DWD GeoServer WMS")
        self.assertEqual(
            self.parsed_capabilities.service_metadata.abstract,
            "This is the Web Map Server of DWD.")
        self.assertEqual(
            self.parsed_capabilities.service_metadata.fees,
            "none"
        )
        self.assertEqual(
            self.parsed_capabilities.service_metadata.access_constraints,
            "http://www.dwd.de/DE/service/copyright/copyright_node.html"
        )

    def _test_service_contact_mapper(self):
        self.assertEqual(
            self.parsed_capabilities.service_metadata.service_contact.name,
            "Deutscher Wetterdienst"
        )
        self.assertEqual(
            self.parsed_capabilities.service_metadata.service_contact.person_name,
            ""
        )
        self.assertEqual(
            self.parsed_capabilities.service_metadata.service_contact.phone,
            ""
        )
        self.assertEqual(
            self.parsed_capabilities.service_metadata.service_contact.facsimile,
            ""
        )
        self.assertEqual(
            self.parsed_capabilities.service_metadata.service_contact.email,
            "info@dwd.de"
        )
        self.assertEqual(
            self.parsed_capabilities.service_metadata.service_contact.country,
            "Germany"
        )
        self.assertEqual(
            self.parsed_capabilities.service_metadata.service_contact.postal_code,
            "63067"
        )
        self.assertEqual(
            self.parsed_capabilities.service_metadata.service_contact.city,
            "Offenbach"
        )
        self.assertEqual(
            self.parsed_capabilities.service_metadata.service_contact.state_or_province,
            "Hessen"
        )
        self.assertEqual(
            self.parsed_capabilities.service_metadata.service_contact.address,
            "Frankfurter Strasse 135"
        )

    def _test_service_keywords(self):
        self.assertEqual(
            self.parsed_capabilities.service_metadata.keywords[0],
            "meteorology"
        )
        self.assertEqual(
            self.parsed_capabilities.service_metadata.keywords[1],
            "climatology"
        )

    def _test_get_capabilities_operation_urls(self):
        self.assertEqual(
            self.parsed_capabilities.operation_urls[0].url,
            "https://maps.dwd.de/geoserver/ows?SERVICE=WMS&"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[0].method,
            "Get"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[0].operation,
            "GetCapabilities"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[0].mime_types[0],
            "text/xml"
        )

        self.assertEqual(
            self.parsed_capabilities.operation_urls[1].url,
            "https://maps.dwd.de/geoserver/ows?SERVICE=WMS&"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[1].method,
            "Post"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[1].operation,
            "GetCapabilities"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[1].mime_types[0],
            "text/xml"
        )

    def _test_get_map_operation_urls(self):
        self.assertEqual(
            self.parsed_capabilities.operation_urls[2].url,
            "https://maps.dwd.de/geoserver/ows?SERVICE=WMS&"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[2].method,
            "Get"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[2].operation,
            "GetMap"
        )
        self.assertEqual(
            len(self.parsed_capabilities.operation_urls[2].mime_types),
            24
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[2].mime_types[0],
            "image/png"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[2].mime_types[1],
            "application/atom+xml"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[2].mime_types[2],
            "application/json;type=geojson"
        )

    def _test_get_feature_info_operation_urls(self):
        self.assertEqual(
            self.parsed_capabilities.operation_urls[3].url,
            "https://maps.dwd.de/geoserver/ows?SERVICE=WMS&"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[3].method,
            "Get"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[3].operation,
            "GetFeatureInfo"
        )
        self.assertEqual(
            len(self.parsed_capabilities.operation_urls[3].mime_types),
            8
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[3].mime_types[0],
            "text/plain"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[3].mime_types[1],
            "application/vnd.ogc.gml"
        )
        self.assertEqual(
            self.parsed_capabilities.operation_urls[3].mime_types[2],
            "text/xml"
        )

    def _test_service_type_mapper(self):
        self.assertEqual(
            self.parsed_capabilities.service_type.version, "1.3.0")
        self.assertEqual(self.parsed_capabilities.service_type.name, "wms")

    def _test_layer_mapper(self):
        self.assertEqual(
            self.parsed_capabilities.root_layer.scale_min,
            4.989528903
        )
        self.assertEqual(
            self.parsed_capabilities.root_layer.scale_max,
            8.7308025
        )
        self.assertEqual(
            self.parsed_capabilities.root_layer.identifier,
            "root_layer"
        )
        self.assertEqual(
            self.parsed_capabilities.root_layer.bbox_lat_lon,
            Polygon(
                (
                    (-180, -90),
                    (-180, 90),
                    (180, 90),
                    (180, -90),
                    (-180, -90)
                )
            )
        )
        self.assertTrue(self.parsed_capabilities.root_layer.is_queryable)
        self.assertTrue(self.parsed_capabilities.root_layer.is_opaque)
        self.assertTrue(self.parsed_capabilities.root_layer.is_cascaded)
        self.assertEqual(
            self.parsed_capabilities.root_layer.parent,
            None
        )
        self.assertEqual(
            self.parsed_capabilities.root_layer.children[0].identifier,
            "Fachlayer"
        )

    def test_wms_xml_mapper(self):
        self._test_root_mapper()
        self._test_service_metadata_mapper()
        self._test_service_contact_mapper()
        self._test_service_keywords()
        self._test_get_capabilities_operation_urls()
        self._test_get_map_operation_urls()
        self._test_get_feature_info_operation_urls()
        self._test_service_type_mapper()
        self._test_layer_mapper()

    def test_wms_operation_urls_append(self):
        o_url = OperationUrl(
            method="Post",
            operation="GetMap",
            mime_types=["image/png"],
            url="http://example.com")

        self.parsed_capabilities.operation_urls.append(
            o_url
        )

        added_operation_url = self.parsed_capabilities.node.xpath(
            "//wms:WMS_Capabilities/wms:Capability/wms:Request/wms:GetMap/wms:DCPType/wms:HTTP/wms:Post/wms:OnlineResource/@xlink:href",
            namespaces={
                "wms": WMS_1_3_0_NAMESPACE,
                "xlink": XLINK_NAMESPACE
            })[0]

        self.assertEqual(
            added_operation_url,
            "http://example.com"
        )

    def test_wms_operation_urls_insert(self):
        o_url = OperationUrl(
            method="Post",
            operation="GetMap",
            mime_types=["image/png"],
            url="http://example.com")

        self.parsed_capabilities.operation_urls.insert(
            0,
            o_url
        )

        added_operation_url = self.parsed_capabilities.node.xpath(
            "//wms:WMS_Capabilities/wms:Capability/wms:Request/wms:GetMap/wms:DCPType/wms:HTTP/wms:Post/wms:OnlineResource/@xlink:href",
            namespaces={
                "wms": WMS_1_3_0_NAMESPACE,
                "xlink": XLINK_NAMESPACE
            })[0]

        self.assertEqual(
            added_operation_url,
            "http://example.com"
        )

    def test_wms_operation_urls_clear(self):
        self.parsed_capabilities.operation_urls.clear()

        operation_urls = self.parsed_capabilities.node.xpath(
            "//wms:WMS_Capabilities/wms:Capability/wms:Request",
            namespaces={
                "wms": WMS_1_3_0_NAMESPACE,
                "xlink": XLINK_NAMESPACE
            })

        self.assertEqual(
            len(self.parsed_capabilities.operation_urls),
            0
        )

        self.assertEqual(
            len(operation_urls),
            0
        )

    def test_wms_operation_urls_pop(self):
        self.parsed_capabilities.operation_urls.pop(1)

        operation_urls = self.parsed_capabilities.node.xpath(
            "//wms:WMS_Capabilities/wms:Capability/wms:Request//wms:DCPType/wms:HTTP/*",
            namespaces={
                "wms": WMS_1_3_0_NAMESPACE,
                "xlink": XLINK_NAMESPACE
            })

        self.assertEqual(
            len(self.parsed_capabilities.operation_urls),
            3
        )

        self.assertEqual(
            len(operation_urls),
            3
        )

    def test_wms_operation_urls_remove(self):

        o_url = self.parsed_capabilities.operation_urls[2]

        self.parsed_capabilities.operation_urls.remove(o_url)

        operation_urls = self.parsed_capabilities.node.xpath(
            "//wms:WMS_Capabilities/wms:Capability/wms:Request//wms:DCPType/wms:HTTP/*",
            namespaces={
                "wms": WMS_1_3_0_NAMESPACE,
                "xlink": XLINK_NAMESPACE
            })

        self.assertEqual(
            len(self.parsed_capabilities.operation_urls),
            3
        )

        self.assertEqual(
            len(operation_urls),
            3
        )

    def test_wms_operation_urls_update_single_object(self):

        o_url = self.parsed_capabilities.operation_urls[0]
        o_url.url = "http://example.com"

        new_o_url_url = self.parsed_capabilities.node.xpath(
            "//wms:WMS_Capabilities/wms:Capability/wms:Request/wms:GetCapabilities/wms:DCPType/wms:HTTP/wms:Get/wms:OnlineResource/@xlink:href",
            namespaces={
                "wms": WMS_1_3_0_NAMESPACE,
                "xlink": XLINK_NAMESPACE
            })[0]

        self.assertEqual(
            new_o_url_url,
            "http://example.com"
        )

    def test_layer_bbox_setter(self):
        new_poly = Polygon(
            (
                (-10, -20),
                (-10, 20),
                (10, 20),
                (10, -20),
                (-10, -20)
            )
        )

        self.parsed_capabilities.root_layer.bbox_lat_lon = new_poly

        root_layer_min_x = self.parsed_capabilities.node.xpath(
            "//wms:WMS_Capabilities/wms:Capability/wms:Layer/wms:EX_GeographicBoundingBox/wms:westBoundLongitude",
            namespaces={
                "wms": WMS_1_3_0_NAMESPACE,
                "xlink": XLINK_NAMESPACE
            })[0]
        root_layer_max_x = self.parsed_capabilities.node.xpath(
            "//wms:WMS_Capabilities/wms:Capability/wms:Layer/wms:EX_GeographicBoundingBox/wms:eastBoundLongitude",
            namespaces={
                "wms": WMS_1_3_0_NAMESPACE,
                "xlink": XLINK_NAMESPACE
            })[0]
        root_layer_min_y = self.parsed_capabilities.node.xpath(
            "//wms:WMS_Capabilities/wms:Capability/wms:Layer/wms:EX_GeographicBoundingBox/wms:southBoundLatitude",
            namespaces={
                "wms": WMS_1_3_0_NAMESPACE,
                "xlink": XLINK_NAMESPACE
            })[0]
        root_layer_max_y = self.parsed_capabilities.node.xpath(
            "//wms:WMS_Capabilities/wms:Capability/wms:Layer/wms:EX_GeographicBoundingBox/wms:northBoundLatitude",
            namespaces={
                "wms": WMS_1_3_0_NAMESPACE,
                "xlink": XLINK_NAMESPACE
            })[0]

        self.assertEqual(
            float(root_layer_min_x.text),
            -10.0
        )
        self.assertEqual(
            float(root_layer_max_x.text),
            10.0
        )
        self.assertEqual(
            float(root_layer_min_y.text),
            -20.0
        )
        self.assertEqual(
            float(root_layer_max_y.text),
            20.0
        )

    def test_camouflage_urls(self):

        self.parsed_capabilities.camouflage_urls(new_domain="example.com")

        new_o_url_url = self.parsed_capabilities.node.xpath(
            "//wms:WMS_Capabilities/wms:Capability/wms:Request/wms:GetCapabilities/wms:DCPType/wms:HTTP/wms:Get/wms:OnlineResource/@xlink:href",
            namespaces={
                "wms": WMS_1_3_0_NAMESPACE,
                "xlink": XLINK_NAMESPACE
            })[0]

        self.assertEqual(
            new_o_url_url,
            "https://example.com/geoserver/ows?SERVICE=WMS&"
        )

    def test_layer_dimension_mapper(self):

        parsed_layer: Layer = self.parsed_capabilities.get_layer_by_identifier(
            "dwd:Autowarn_Analyse")

        parsed_extent: TimeExtent = parsed_layer.dimensions[0].time_extents[0]

        self.assertEqual(
            parsed_extent.start,
            parse_datetime("2021-11-29T12:40:00.000Z")
        )
        self.assertEqual(
            parsed_extent.stop,
            parse_datetime("2021-12-13T12:40:00.000Z")
        )
        self.assertEqual(
            parsed_extent.resolution,
            parse_duration("PT5M")
        )

    def test_layer_dimension_time_extent_setter_with_list_of_intervals(self):

        new_time_extend = TimeExtent(
            start=parse_datetime("2020-11-29T12:40:00Z"),
            stop=parse_datetime("2021-12-13T12:40:00Z"),
            resolution=parse_duration("P1D")
        )

        parsed_layer: Layer = self.parsed_capabilities.get_layer_by_identifier(
            "dwd:Autowarn_Analyse")

        parsed_layer.dimensions[0].time_extents = [new_time_extend]

        new_time_extent_value = self.parsed_capabilities.node.xpath(
            "//wms:WMS_Capabilities/wms:Capability//wms:Layer[wms:Name='dwd:Autowarn_Analyse']/wms:Dimension",
            namespaces={
                "wms": WMS_1_3_0_NAMESPACE,
                "xlink": XLINK_NAMESPACE
            })[0]

        self.assertEqual(
            new_time_extent_value.text,
            "2020-11-29T12:40:00Z/2021-12-13T12:40:00Z/P1D"
        )

    def test_layer_dimension_time_extent_append_with_list_of_intervals(self):

        new_time_extend = TimeExtent(
            start=parse_datetime("2020-11-29T12:40:00Z"),
            stop=parse_datetime("2021-12-13T12:40:00Z"),
            resolution=parse_duration("P1D")
        )

        parsed_layer: Layer = self.parsed_capabilities.get_layer_by_identifier(
            "dwd:Autowarn_Analyse")

        parsed_layer.dimensions[0].time_extents.append(new_time_extend)

        new_time_extent_value = self.parsed_capabilities.node.xpath(
            "//wms:WMS_Capabilities/wms:Capability//wms:Layer[wms:Name='dwd:Autowarn_Analyse']/wms:Dimension",
            namespaces={
                "wms": WMS_1_3_0_NAMESPACE,
                "xlink": XLINK_NAMESPACE
            })[0]

        self.assertEqual(
            new_time_extent_value.text,
            "2021-11-29T12:40:00Z/2021-12-13T12:40:00Z/PT5M,2020-11-29T12:40:00Z/2021-12-13T12:40:00Z/P1D"
        )

    def test_layer_layers_property(self):
        self.assertEqual(
            len(self.parsed_capabilities.layers),
            137
        )
