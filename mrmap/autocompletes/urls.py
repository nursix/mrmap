from django.urls import path
from autocompletes import autocompletes


app_name = 'autocompletes'
urlpatterns = [
    path('kw/', autocompletes.KeywordAutocomplete.as_view(create_field="keyword"), name="keyword"),
    path('cat/', autocompletes.CategoryAutocomplete.as_view(), name="category"),

    path('md/', autocompletes.MetadataAutocomplete.as_view(), name="metadata"),
    path('md-s/', autocompletes.MetadataServiceAutocomplete.as_view(), name="metadata_service"),
    path('md-d/', autocompletes.MetadataDatasetAutocomplete.as_view(), name="metadata_dataset"),
    path('md-l/', autocompletes.MetadataLayerAutocomplete.as_view(), name="metadata_layer"),
    path('md-ft/', autocompletes.MetadataFeaturetypeAutocomplete.as_view(), name="metadata_featuretype"),
    path('md-c/', autocompletes.MetadataCatalougeAutocomplete.as_view(), name="metadata_catalouge"),
    path('md-contact/', autocompletes.MetadataContactAutocomplete.as_view(), name="metadata_contacts"),

    path('perm/', autocompletes.PermissionsAutocomplete.as_view(), name="permissions"),

    path('orga/', autocompletes.OrganizationAutocomplete.as_view(), name="organizations"),

    path('acl/', autocompletes.AccessControlListAutocomplete.as_view(), name="accesscontrollists"),

    path('rs/', autocompletes.ReferenceSystemAutocomplete.as_view(), name="reference_system"),
    path('ops/', autocompletes.OperationsAutocomplete.as_view(), name="operations"),
    path('users/', autocompletes.UsersAutocomplete.as_view(), name="users"),

    path('monitoring-run/', autocompletes.MonitoringRunAutocomplete.as_view(), name="monitoring_run"),
    path('monitoring-res/', autocompletes.MonitoringResultAutocomplete.as_view(), name="monitoring_result"),
    path('monitoring-hs/', autocompletes.HealthStateAutocomplete.as_view(), name="monitoring.healthstate"),

]
