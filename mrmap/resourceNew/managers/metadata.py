from django.db import models, transaction, OperationalError
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from resourceNew.enums.metadata import MetadataOriginEnum, MetadataRelationEnum, MetadataOrigin
from django.utils import timezone


class LicenceManager(models.Manager):
    """
    handles the creation of objects by using the parsed service which is stored in the given :class:`new.Service`
    instance.
    """

    def as_choices(self) -> list:
        """ Returns a list of (identifier, name) to be used as choices in a form

        Returns:
             tuple_list (list): As described above
        """
        return [(licence.identifier, licence.__str__()) for licence in self.get_queryset().filter(is_active=True)]

    def get_descriptions_help_text(self):
        """ Returns a string containing all Licence records for rendering as help_text in a form

        Returns:
             string (str): As described above
        """
        from django.db.utils import ProgrammingError

        try:
            descrs = [
                "<a href='{}' target='_blank'>{}</a>".format(
                    licence.description_url, licence.identifier
                ) for licence in self.get_queryset().all()
            ]
            descr_str = "<br>".join(descrs)
            descr_str = _("Explanations: <br>") + descr_str
        except (ProgrammingError, OperationalError):
            # This will happen on an initial installation. The Licence table won't be created yet, but this function
            # will be called on makemigrations.
            descr_str = ""
        return descr_str


class IsoMetadataManager(models.Manager):
    """ IsoMetadataManager to handle creation of

    """
    keyword_cls = None
    metadata_contact_cls = None
    dataset_contact_cls = None

    def _reset_local_variables(self):
        self.keyword_cls = None

    def _create_contact(self, contact):
        contact, created = contact.get_model_class().objects.get_or_create(**contact.get_field_dict())
        return contact

    def _create_dataset_metadata(self, parsed_metadata, origin_url):
        db_metadata_contact = self._create_contact(contact=parsed_metadata.metadata_contact)
        db_dataset_contact = self._create_contact(contact=parsed_metadata.dataset_contact)

        field_dict = parsed_metadata.get_field_dict()

        try:
            db_dataset_metadata = self.model.objects.get(dataset_id=field_dict["dataset_id"],
                                                         dataset_id_code_space=field_dict["dataset_id_code_space"])

            dt_aware = timezone.make_aware(field_dict["date_stamp"], timezone.get_current_timezone())
            if dt_aware > db_dataset_metadata.date_stamp:
                db_dataset_metadata.objects.update(metadata_contact=db_metadata_contact,
                                                   dataset_contact=db_dataset_contact,
                                                   **field_dict)
        except ObjectDoesNotExist:
            db_dataset_metadata = super().create(metadata_contact=db_metadata_contact,
                                                 dataset_contact=db_dataset_contact,
                                                 origin=MetadataOrigin.ISO_METADATA.value,
                                                 origin_url=origin_url,
                                                 **field_dict)
        return db_dataset_metadata

    def _create_service_metadata(self, parsed_metadata, *args, **kwargs):
        db_metadata_contact = self._create_contact(contact=parsed_metadata.metadata_contact).save()

        db_service_metadata = super().create(metadata_contact=db_metadata_contact,
                                             *args,
                                             **kwargs)
        return db_service_metadata

    def create_from_parsed_metadata(self, parsed_metadata, related_object, origin_url, *args, **kwargs):
        self._reset_local_variables()
        with transaction.atomic():

            if parsed_metadata.hierarchy_level == "service":
                # todo: update instead of creating, cause we generate service metadata records out of the box from
                #  capabilitites
                db_metadata = self._create_service_metadata(parsed_metadata=parsed_metadata, *args, **kwargs)
            else:
                db_metadata = self._create_dataset_metadata(parsed_metadata=parsed_metadata, origin_url=origin_url)
                db_metadata.add_dataset_metadata_relation(relation_type=MetadataRelationEnum.DESCRIBES.value,
                                                          related_object=related_object,
                                                          origin=MetadataOriginEnum.CAPABILITIES.value)
            db_keyword_list = []
            if not self.keyword_cls:
                self.keyword_cls = parsed_metadata.keywords[0].get_model_class()
            for keyword in parsed_metadata.keywords:
                db_keyword, created = self.keyword_cls.objects.get_or_create(**keyword.get_field_dict())
                db_keyword_list.append(db_keyword)
            db_metadata.keywords.add(*db_keyword_list)


            # todo: ref systems
            # todo: categories

            return db_metadata
