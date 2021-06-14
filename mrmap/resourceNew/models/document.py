from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from main.models import CommonInfo
from resourceNew.models import ServiceMetadata, LayerMetadata, FeatureTypeMetadata, DatasetMetadata, Service
from eulxml import xmlmap

from resourceNew.parsers.iso.iso_metadata import WrappedIsoMetadata


class Document(CommonInfo):
    HELP_TEXT = _("the metadata object which is parsed from this xml.")
    uuid = models.SlugField(editable=False)
    service = models.ForeignKey(to=Service,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True,
                                related_name="documents",
                                related_query_name="document",
                                verbose_name=_("related service"),
                                help_text=_("the service object which is described by this document."))
    service_metadata = models.ForeignKey(to=ServiceMetadata,
                                         on_delete=models.CASCADE,
                                         null=True,
                                         blank=True,
                                         related_name="documents",
                                         related_query_name="document",
                                         verbose_name=_("related dataset metadata"),
                                         help_text=HELP_TEXT)
    layer_metadata = models.ForeignKey(to=LayerMetadata,
                                       on_delete=models.CASCADE,
                                       null=True,
                                       blank=True,
                                       related_name="documents",
                                       related_query_name="document",
                                       verbose_name=_("related layer metadata"),
                                       help_text=HELP_TEXT)
    feature_type_metadata = models.ForeignKey(to=FeatureTypeMetadata,
                                              on_delete=models.CASCADE,
                                              null=True,
                                              blank=True,
                                              related_name="documents",
                                              related_query_name="document",
                                              verbose_name=_("related feature type metadata"),
                                              help_text=HELP_TEXT)
    dataset_metadata = models.ForeignKey(to=DatasetMetadata,
                                         on_delete=models.CASCADE,
                                         null=True,
                                         blank=True,
                                         related_name="documents",
                                         related_query_name="document",
                                         verbose_name=_("related dataset metadata"),
                                         help_text=HELP_TEXT)
    content = models.TextField(verbose_name=_("content"),
                               help_text=_("the xml as string."))
    is_original = models.BooleanField(default=False,
                                      verbose_name=_("is original?"),
                                      help_text=_("check if this document is the original xml."))

    class Meta:
        # One Metadata/Service object can be related to multiple Document objects, cause we save the original and the
        # customized version of a given xml.
        # But one Metadata object can only have one Document which is original
        constraints = [
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_one_original",
                fields=("service",
                        "service_metadata",
                        "layer_metadata",
                        "feature_type_metadata",
                        "dataset_metadata",
                        "is_original",)
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_one_related_object_selected",
                check=Q(
                    (Q(service=False,
                       service_metadata=False,
                       layer_metadata=False,
                       feature_type_metadata=False,
                       dataset_metadata=False) |
                     Q(service=True,
                       service_metadata=False,
                       layer_metadata=False,
                       feature_type_metadata=False,
                       dataset_metadata=False) |
                     Q(service=False,
                       service_metadata=True,
                       layer_metadata=False,
                       feature_type_metadata=False,
                       dataset_metadata=False) |
                     Q(service=False,
                       service_metadata=False,
                       layer_metadata=True,
                       feature_type_metadata=False,
                       dataset_metadata=False) |
                     Q(service=False,
                       service_metadata=False,
                       layer_metadata=False,
                       feature_type_metadata=True,
                       dataset_metadata=False) |
                     Q(service=False,
                       service_metadata=False,
                       layer_metadata=False,
                       feature_type_metadata=False,
                       dataset_metadata=True))
                    and ~Q(Q(service=True)
                           and Q(service_metadata=True)
                           and Q(layer_metadata=True)
                           and Q(feature_type_metadata=True)
                           and Q(dataset_metadata=True))
                    and ~Q(Q(service=False)
                           and Q(service_metadata=False)
                           and Q(layer_metadata=False)
                           and Q(feature_type_metadata=False)
                           and Q(dataset_metadata=False))
                )
            ),
        ]

    def __str__(self):
        return f"{self.related_object} (document) | {self.is_original}"

    def save(self, *args, **kwargs):
        adding = False
        if self._state.adding:
            adding = True
        super().save(*args, **kwargs)
        if adding and self.is_original:
            Document.objects.create(**self.get_copy_fields_dict())

    def clean(self):
        """ Raise ValidationError if service metadata, layer metadata, feature type metadata and dataset metadata are
            selected OR if none of them are selected.
        """
        msg = _("multiple or empty selections for related objects are not supported. Select only one of service "
                "metadata or a layer metadata or a feature type metadata or a dataset metadata.")
        supported_conditions = [(self.service
                                 and not self.service_metadata
                                 and not self.layer_metadata
                                 and not self.feature_type_metadata
                                 and not self.dataset_metadata),
                                (not self.service
                                 and self.service_metadata
                                 and not self.layer_metadata
                                 and not self.feature_type_metadata
                                 and not self.dataset_metadata),
                                (not self.service
                                 and not self.service_metadata
                                 and self.layer_metadata
                                 and not self.feature_type_metadata
                                 and not self.dataset_metadata),
                                (not self.service
                                 and not self.service_metadata
                                 and not self.layer_metadata
                                 and self.feature_type_metadata
                                 and not self.dataset_metadata),
                                (not self.service
                                 and not self.service_metadata
                                 and not self.layer_metadata
                                 and not self.feature_type_metadata
                                 and self.dataset_metadata)]
        for supported_condition in supported_conditions:
            if supported_condition:
                return
        raise ValidationError(msg)

    @property
    def related_object(self):
        if self.service:
            return self.service
        elif self.service_metadata:
            return self.service_metadata
        elif self.layer_metadata:
            return self.layer_metadata
        elif self.feature_type_metadata:
            return self.feature_type_metadata
        elif self.dataset_metadata:
            return self.dataset_metadata

    def get_copy_fields_dict(self):
        return {"uuid": self.uuid,
                "is_original": False,
                "content": self.content,
                "service": self.service,
                "service_metadata": self.service_metadata,
                "layer_metadata": self.layer_metadata,
                "feature_type_metadata":self.feature_type_metadata,
                "dataset_metadata": self.dataset_metadata}

    def update_xml_content(self, related_object=None):
        if not related_object:
            related_object = self.related_object
        parsed_metadata = xmlmap.load_xmlobject_from_string(string=bytes(self.content, 'utf-8'),
                                                            xmlclass=WrappedIsoMetadata)
        parsed_metadata.iso_metadata.update_fields_from_db_object(db_object=related_object)
        self.content = str(parsed_metadata.serializeDocument(), "UTF-8")
        self.save()
