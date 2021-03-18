"""
Core models to implement the possibility of Roles

For more information on this file, see
# todo: link to the docs

"""

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _


class TemplateRole(models.Model):
    """`TemplateRole` model to handle of one or more permissions as a template for a given `ContentType`.
    Use this model to construct your custom roles.
    """
    verbose_name = models.CharField(max_length=58,
                                    verbose_name=_("Verbose name"),
                                    help_text=_("The verbose name of the role"))
    description = models.TextField(verbose_name=_("Description"),
                                   help_text=_("Describe what permissions this role shall grant"))
    permissions = models.ManyToManyField(to=Permission, related_name='role_set')
    content_type = models.ForeignKey(to=ContentType, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.verbose_name)


class ObjectBasedTemplateRole(Group):
    """ ObjectBasedTemplateRole model to handle Role groups per object.
    On object creation, one `ObjectBasedRoleGroup` per defined `Role` is generated.
    NOTE !!: do not create or change instance of this model manual.
      This `Permission` `Group`s are generated by permission/signals.py
    """
    object_pk = models.CharField(_('object ID'), max_length=255)
    content_object = GenericForeignKey(fk_field='object_pk')
    content_type = models.ForeignKey(to=ContentType, on_delete=models.CASCADE)
    # do not change after generation of this instance, cause permission changing is not implemented for base_template
    # changing.
    based_template = models.ForeignKey(to=TemplateRole, on_delete=models.CASCADE,
                                       related_name='object_based_template_roles')
    description = models.TextField(verbose_name=_("Description"),
                                   help_text=_("Describe what permissions this role shall grant"))

    def __str__(self):
        return '{} | {} | {}'.format(
                str(self.content_object),
                str(self.name),
                str([perm.codename for perm in self.based_template.permissions.all()]))

    def save(self, *args, **kwargs):
        adding = self._state.adding
        if adding:
            self.name = f'{self.content_object} | {self.based_template.verbose_name}'
            self.description = _('handle permissions based on the "').__str__() + self.based_template.__str__() + _(
                '" `TemplateRole` for "').__str__() + self.content_object.__str__() + '"'
        super().save(*args, **kwargs)


