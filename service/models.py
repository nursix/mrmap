import datetime
from django.db import models
from django.contrib.gis.db import models

from structure.models import User, Group, Organization


class Keyword(models.Model):
    keyword = models.CharField(max_length=255)

    def __str__(self):
        return self.keyword


class Metadata(models.Model):
    uuid = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    abstract = models.CharField(max_length=1000, null=True, blank=True)
    online_resource = models.CharField(max_length=255, null=True)
    is_root = models.BooleanField(default=False)
    # Service md
    service = models.OneToOneField('Service', null=True, blank=True, on_delete=models.CASCADE)
    contact_person = models.CharField(max_length=100, null=True)
    contact_person_position = models.CharField(max_length=100, null=True)
    contact_organization = models.CharField(max_length=100, null=True)
    address_type = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    state_or_province = models.CharField(max_length=100, null=True)
    post_code = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    contact_phone = models.CharField(max_length=100, null=True)
    contact_email = models.CharField(max_length=100, null=True)
    terms_of_use = models.ForeignKey('TermsOfUse', on_delete=models.DO_NOTHING, null=True)
    access_constraints = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    last_change = models.DateTimeField(null=True)
    status = models.IntegerField(null=True)
    last_harvest_successful = models.BooleanField(null=True)
    last_harvest_exception = models.CharField(max_length=200, null=True)
    export_to_csw = models.BooleanField(default=False)
    spatial_res_type = models.CharField(max_length=100, null=True)
    spatial_res_value = models.CharField(max_length=100, null=True)
    is_active = models.BooleanField(default=False)
    is_inspire_conform = models.BooleanField(default=False)
    has_inspire_downloads = models.BooleanField(default=False)
    geom = models.GeometryField(null=True)
    bounding_geometry = models.GeometryField(null=True)
    # capabilities
    bbox = models.DecimalField(decimal_places=2, max_digits=4, null=True)
    dimension = models.CharField(max_length=100, null=True)
    authority_url = models.CharField(max_length=255, null=True)
    identifier = models.CharField(max_length=255, null=True)
    metadata_url = models.CharField(max_length=255, null=True)
    # other
    keywords = models.ManyToManyField(Keyword)
    reference_system = models.ManyToManyField('ReferenceSystem')

    def __str__(self):
        return str(self.uuid)


# class KeywordToMetadata(models.Model):
#     metadata = models.ForeignKey(Metadata, on_delete=models.CASCADE)
#     keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.keyword.keyword


class TermsOfUse(models.Model):
    #service = models.ForeignKey('Service', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    symbol_url = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    is_open_data = models.BooleanField()
    fees = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    title_DE = models.CharField(max_length=100, unique=True)
    title_EN = models.CharField(max_length=100, unique=True)
    description_DE = models.CharField(max_length=100, unique=True)
    description_EN = models.CharField(max_length=100, unique=True)
    is_inspire = models.BooleanField()
    symbol = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField()
    created = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title_EN


class ServiceType(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=100)
    specification = models.URLField(blank=False, null=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    parent_service = models.ForeignKey('self', on_delete=models.CASCADE, related_name="child_service", null=True)
    published_for = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, related_name="published_for")
    published_by = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, related_name="published_by")
    registered_by = models.ForeignKey(Group, on_delete=models.DO_NOTHING, related_name="registered_services")
    servicetype = models.ForeignKey(ServiceType, on_delete=models.DO_NOTHING, blank=True)
    categories = models.ManyToManyField(Category)
    availability = models.DecimalField(decimal_places=2, max_digits=4, default=0.0)
    is_available = models.BooleanField(default=False)
    get_capabilities_uri = models.CharField(max_length=1000, null=True)
    get_map_uri = models.CharField(max_length=1000, null=True)
    get_feature_info_uri = models.CharField(max_length=1000, null=True)
    describe_layer_uri = models.CharField(max_length=1000, null=True)
    get_legend_graphic_uri = models.CharField(max_length=1000, null=True)
    get_styles_uri = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return str(self.id)


class Layer(Service):
    identifier = models.CharField(max_length=500, null=True)
    hits = models.IntegerField(default=0)
    preview_image = models.CharField(max_length=100)
    preview_extend = models.CharField(max_length=100)
    preview_legend = models.CharField(max_length=100)
    parent_layer = models.ForeignKey("self", on_delete=models.CASCADE, null=True, related_name="child_layer")
    position = models.IntegerField(default=0)
    is_queryable = models.BooleanField(default=False)
    is_opaque = models.BooleanField(default=False)
    is_cascaded = models.BooleanField(default=False)
    scale_min = models.FloatField(default=0)
    scale_max = models.FloatField(default=0)
    bbox_lat_lon = models.CharField(max_length=255, default='{"minx":-90.0, "miny":-180.0, "maxx": 90.0, "maxy":180.0}')

    def __str__(self):
        return str(self.identifier)


class Module(Service):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type


class ReferenceSystem(models.Model):
    code = models.CharField(max_length=100)
    prefix = models.CharField(max_length=255, default="EPSG:")
    version = models.CharField(max_length=50, default="9.6.1")

    def __str__(self):
        return self.code


# class ReferenceSystemToMetadata(models.Model):
#     metadata = models.ForeignKey(Metadata, on_delete=models.CASCADE)
#     reference_system = models.ForeignKey(ReferenceSystem, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.reference_system.code


class Dataset(models.Model):
    time_begin = models.DateTimeField()
    time_end = models.DateTimeField()


class ServiceToFormat(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="formats")
    action = models.CharField(max_length=255, null=True)
    mime_type = models.CharField(max_length=500)

    def __str__(self):
        return self.mime_type


class Dimension(models.Model):
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    units = models.CharField(max_length=255)
    default = models.CharField(max_length=255)
    nearest_value = models.CharField(max_length=255)
    current = models.CharField(max_length=255)
    extent = models.CharField(max_length=500)
    inherited = models.BooleanField()

    def __str__(self):
        return self.layer.name + ": " + self.name


class Style(models.Model):
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    uri = models.CharField(max_length=500)
    height = models.IntegerField()
    width = models.IntegerField()
    mime_type = models.CharField(max_length=500)

    def __str__(self):
        return self.layer.name + ": " + self.name


class FeatureType(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    abstract = models.TextField(null=True)
    searchable = models.BooleanField(default=False)
    default_srs = models.ForeignKey(ReferenceSystem, on_delete=models.DO_NOTHING, null=True, related_name="default_srs")
    inspire_download = models.BooleanField(default=False)
    bbox_lat_lon = models.CharField(max_length=255, default='{"minx":-90.0, "miny":-180.0, "maxx": 90.0, "maxy":180.0}')
    keywords = models.ManyToManyField(Keyword)
    reference_system = models.ManyToManyField(ReferenceSystem)



# class KeywordToFeatureType(models.Model):
#     feature_type = models.ForeignKey(FeatureType, on_delete=models.CASCADE)
#     keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
#
#
# class ReferenceSystemToFeatureType(models.Model):
#     feature_type = models.ForeignKey(FeatureType, on_delete=models.CASCADE)
#     reference_system = models.ForeignKey(ReferenceSystem, on_delete=models.CASCADE)
