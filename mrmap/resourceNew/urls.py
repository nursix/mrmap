from django.urls import path
from resourceNew.views import service as service_views
from resourceNew.views import metadata as metadata_views
from resourceNew.views import document as document_views

app_name = 'resourceNew'
urlpatterns = [
    path("service/add", service_views.RegisterServiceFormView.as_view(), name="service_add"),
    path("service/wms", service_views.WmsListView.as_view(), name="service_wms_list"),
    path("service/layers", service_views.LayerListView.as_view(), name="layer_list"),
    path("service/wfs", service_views.WfsListView.as_view(), name="service_wfs_list"),
    path("service/featuretypes", service_views.FeatureTypeListView.as_view(), name="feature_type_list"),
    path("service/featuretypeelements", service_views.FeatureTypeElementListView.as_view(), name="feature_type_element_list"),

    path("service/<pk>", service_views.ServiceTreeView.as_view(), name="service_view"),
    path("service/<pk>/change", service_views.ServiceUpdateView.as_view(), name="service_change"),

    path("metadata/services", metadata_views.ServiceMetadataListView.as_view(), name="service_metadata_list"),
    path("metadata/layers", metadata_views.LayerMetadataListView.as_view(), name="layer_metadata_list"),
    path("metadata/featuretypes", metadata_views.FeatureTypeMetadataListView.as_view(), name="feature_type_metadata_list"),
    path("metadata/datasets", metadata_views.DatasetMetadataListView.as_view(), name="dataset_metadata_list"),

    path("metadata/services/<pk>/change", metadata_views.ServiceMetadataUpdateView.as_view(), name="service_metadata_change"),
    path("metadata/datasets/<pk>/change", metadata_views.DatasetMetadataUpdateView.as_view(), name="dataset_metadata_change"),

    path("documents/<slug:uuid>", document_views.DocumentDetailView.as_view(), name="document_view")
]

