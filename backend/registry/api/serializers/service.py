
from registry.api.serializers.metadata import (KeywordSerializer,
                                               StyleSerializer)
from registry.models.metadata import Keyword, Style
from registry.models.service import (FeatureType, Layer, OgcService,
                                     OperationUrl, WebFeatureService,
                                     WebMapService)
from rest_framework.fields import BooleanField
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework_gis.fields import GeometryField
from rest_framework_json_api.relations import (HyperlinkedRelatedField,
                                               ResourceRelatedField)
from rest_framework_json_api.serializers import (ModelSerializer,
                                                 PolymorphicModelSerializer)
from users.models.groups import Organization


class OperationsUrlSerializer(ModelSerializer):

    class Meta:
        model = OperationUrl
        fields = '__all__'


class LayerSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='registry:layer-detail',
    )

    bbox_lat_lon = GeometryField()
    styles = HyperlinkedRelatedField(
        queryset=Style.objects,
        many=True,  # necessary for M2M fields & reverse FK fields
        related_link_view_name='registry:layer-styles-list',
        related_link_url_kwarg='parent_lookup_layer',
        self_link_view_name='registry:layer-relationships',
    )
    keywords = HyperlinkedRelatedField(
        queryset=Keyword.objects,
        many=True,  # necessary for M2M fields & reverse FK fields
        related_link_view_name='registry:layer-keywords-list',
        related_link_url_kwarg='parent_lookup_layer',
        self_link_view_name='registry:layer-relationships',
    )

    included_serializers = {
        'styles': StyleSerializer,
        'keywords': KeywordSerializer,
    }

    class Meta:
        model = Layer
        fields = '__all__'


class WebMapServiceSerializer(ModelSerializer):

    url = HyperlinkedIdentityField(
        view_name='registry:wms-detail',
    )

    layers = HyperlinkedRelatedField(
        queryset=Layer.objects,
        many=True,  # necessary for M2M fields & reverse FK fields
        related_link_view_name='registry:wms-layers-list',
        related_link_url_kwarg='parent_lookup_service',
        self_link_view_name='registry:wms-relationships',
        required=False,
    )

    included_serializers = {
        'layers': LayerSerializer,
    }

    class Meta:
        model = WebMapService
        fields = "__all__"


class FeatureTypeSerializer(ModelSerializer):

    keywords = HyperlinkedRelatedField(
        queryset=Keyword.objects,
        many=True,  # necessary for M2M fields & reverse FK fields
        related_link_view_name='registry:featuretype-keywords-list',
        related_link_url_kwarg='parent_lookup_featuretype',
        self_link_view_name='registry:featuretype-relationships',
    )

    included_serializers = {
        'keywords': KeywordSerializer,
    }

    class Meta:
        model = FeatureType
        fields = '__all__'


class WebFeatureServiceSerializer(ModelSerializer):

    url = HyperlinkedIdentityField(
        view_name='registry:wfs-detail',
    )

    included_serializers = {
        'featuretypes': FeatureTypeSerializer,
    }

    featuretypes = HyperlinkedRelatedField(
        queryset=FeatureType.objects,
        many=True,  # necessary for M2M fields & reverse FK fields
        related_link_view_name='registry:wfs-featuretypes-list',
        related_link_url_kwarg='parent_lookup_service',
        self_link_view_name='registry:wfs-relationships',
    )

    class Meta:
        model = WebFeatureService
        fields = "__all__"


class OgcServiceSerializer(PolymorphicModelSerializer):
    polymorphic_serializers = [
        WebMapServiceSerializer, WebFeatureServiceSerializer]

    class Meta:
        model = OgcService
        fields = "__all__"


class OgcServiceCreateSerializer(ModelSerializer):

    # TODO: implement included serializer for ServiceAuthentication
    # included_serializers = {
    #     'auth': ServiceAuthentication,
    # }
    owned_by_org = ResourceRelatedField(
        queryset=Organization.objects,
    )

    collect_metadata_records = BooleanField(default=True)

    class Meta:
        model = OgcService
        fields = ("get_capabilities_url", "owned_by_org",
                  "collect_metadata_records")
