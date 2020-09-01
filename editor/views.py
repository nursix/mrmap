from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Case, When
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from MrMap.decorator import check_permission, check_ownership
from MrMap.messages import SECURITY_PROXY_WARNING_ONLY_FOR_ROOT
from MrMap.responses import DefaultContext
from editor.filters import EditorAccessFilter
from editor.forms import MetadataEditorForm, RemoveDatasetForm, RestoreMetadataForm, RestoreDatasetMetadata, \
    RestrictAccessForm, RestrictAccessSpatially
from editor.tables import EditorAcessTable
from editor.wizards import DATASET_WIZARD_FORMS, DatasetWizard
from service.models import MetadataRelation
from service.helper.enums import MetadataEnum, ResourceOriginEnum
from service.models import Metadata
from structure.models import MrMapGroup
from structure.permissionEnums import PermissionEnum
from users.helper import user_helper


@login_required
@check_permission(PermissionEnum.CAN_REMOVE_DATASET_METADATA)
@check_ownership(Metadata, 'metadata_id')
def remove_dataset(request: HttpRequest, metadata_id):
    """ The remove view for dataset metadata

    Args:
        request: The incoming request
        metadata_id: The metadata id
    Returns:
        A rendered view
    """
    metadata = get_object_or_404(Metadata, id=metadata_id)
    if metadata.metadata_type != MetadataEnum.DATASET.value:
        messages.success(request, message=_("You can't delete metadata record"))
        return HttpResponseRedirect(reverse(request.GET.get('current-view', 'home'), ), status=303)

    relations = MetadataRelation.objects.filter(metadata_to=metadata)
    is_mr_map_origin = True
    for relation in relations:
        if relation.origin != ResourceOriginEnum.EDITOR.value:
            is_mr_map_origin = False
            break
    if is_mr_map_origin is not True:
        messages.success(request, message=_("You can't delete autogenerated datasets"))
        return HttpResponseRedirect(reverse(request.GET.get('current-view', 'home'), ), status=303)

    form = RemoveDatasetForm(data=request.POST or None,
                             request=request,
                             reverse_lookup='editor:remove-dataset-metadata',
                             reverse_args=[metadata_id, ],
                             # ToDo: after refactoring of all forms is done, show_modal can be removed
                             show_modal=True,
                             is_confirmed_label=_("Do you really want to delete this dataset?"),
                             instance=metadata)
    return form.process_request(valid_func=form.process_remove_dataset)


@login_required
@check_permission(
    PermissionEnum.CAN_ADD_DATASET_METADATA
)
def add_new_dataset_wizard(request: HttpRequest, ):
    return DatasetWizard.as_view(form_list=DATASET_WIZARD_FORMS,
                                 ignore_uncomitted_forms=True,
                                 current_view=request.GET.get('current-view'),
                                 title=_(format_html('<b>Add New Dataset</b>')),
                                 id_wizard='add_new_dataset_wizard',
                                 )(request=request)


@login_required
@check_permission(PermissionEnum.CAN_EDIT_METADATA)
@check_ownership(Metadata, 'metadata_id')
def edit_dataset_wizard(request, metadata_id):
    metadata = get_object_or_404(Metadata,
                                 ~Q(metadata_type=MetadataEnum.CATALOGUE.value),
                                 id=metadata_id)
    return DatasetWizard.as_view(form_list=DATASET_WIZARD_FORMS,
                                 ignore_uncomitted_forms=True,
                                 current_view=request.GET.get('current-view'),
                                 current_view_arg=request.GET.get('current-view-arg', None),
                                 instance_id=metadata_id,
                                 title=_(format_html(f'<b>Edit</b> <i>{metadata.title}</i> <b>Dataset</b>')),
                                 id_wizard=f'edit_{metadata.id}_dataset_wizard',
                                 )(request=request)


@login_required
@check_permission(
    PermissionEnum.CAN_EDIT_METADATA
)
@check_ownership(Metadata, 'metadata_id')
def edit(request: HttpRequest, metadata_id):
    """ The edit view for metadata

    Provides editing functions for all elements which are described by Metadata objects

    Args:
        request: The incoming request
        metadata_id: The metadata id
    Returns:
        A rendered view
    """
    metadata = get_object_or_404(Metadata,
                                 ~Q(metadata_type=MetadataEnum.CATALOGUE.value),
                                 id=metadata_id,)
    if metadata.metadata_type == MetadataEnum.DATASET.value:
        return HttpResponseRedirect(reverse("editor:edit-dataset-metadata", args=(metadata_id,)), status=303)

    form = MetadataEditorForm(data=request.POST or None,
                              instance=metadata,
                              request=request,
                              reverse_lookup='editor:edit',
                              reverse_args=[metadata_id, ],
                              # ToDo: after refactoring of all forms is done, show_modal can be removed
                              show_modal=True,
                              has_autocomplete_fields=True,
                              form_title=_("Edit metadata <strong>{}</strong>").format(metadata.title)
                              )
    return form.process_request(valid_func=form.process_edit_metadata)


@login_required
@check_permission(
    PermissionEnum.CAN_EDIT_METADATA
)
@check_ownership(Metadata, 'object_id')
def edit_access(request: HttpRequest, object_id, update_params: dict = None, status_code: int = 200,):
    """ The edit view for the operations access

    Provides a form to set the access permissions for a metadata-related object.
    Processes the form input afterwards

    Args:
        request (HttpRequest): The incoming request
        id (int): The metadata id
    Returns:
         A rendered view
    """
    template = "views/editor_edit_access_index.html"
    user = user_helper.get_user(request)
    md = get_object_or_404(Metadata,
                           ~Q(metadata_type=MetadataEnum.CATALOGUE.value),
                           id=object_id)
    is_root = md.is_root()

    form = RestrictAccessForm(
        data=request.POST or None,
        request=request,
        action_url=reverse('editor:edit_access', args=[object_id, ], ),
        metadata=md
    )

    all_groups = MrMapGroup.objects.all().order_by(
        Case(
            When(
                name='Public',
                then=0
            )
        ),
        'name'
    )

    table = EditorAcessTable(
        request=request,
        queryset=all_groups,
        filter_set_class=EditorAccessFilter,
        current_view='editor:edit_access',
        related_metadata=md,
    )

    params = {
        "restrict_access_form": form,
        "restrict_access_table": table,
        "service_metadata": md,
        "is_root": is_root,
    }

    if request.method == 'POST':
        # Check if update form is valid or action is performed on a root metadata
        if not is_root:
            messages.error(request, SECURITY_PROXY_WARNING_ONLY_FOR_ROOT)
        elif form.is_valid():
            form.process_securing_access(md)

    if update_params:
        params.update(update_params)

    context = DefaultContext(request, params, user)
    return render(request=request,
                  template_name=template,
                  context=context.get_context(),
                  status=status_code)


@login_required
def access_geometry_form(request: HttpRequest, metadata_id, group_id):
    """ Renders the geometry form for the access editing

    Args:
        request (HttpRequest): The incoming request
        metadata_id (int): The id of the metadata object, which will be edited
        group_id:
    Returns:

    """
    get_object_or_404(Metadata,
                      ~Q(metadata_type=MetadataEnum.CATALOGUE.value),
                      id=metadata_id)
    group = get_object_or_404(MrMapGroup, id=group_id)
    form = RestrictAccessSpatially(
        data=request.POST or None,
        request=request,
        reverse_lookup='editor:access_geometry_form',
        reverse_args=[metadata_id, group_id],
        # ToDo: after refactoring of all forms is done, show_modal can be removed
        show_modal=True,
        form_title=_(f"Edit spatial area for group <strong>{group.name}</strong>"),
        metadata_id=metadata_id,
        group_id=group_id,
    )
    return form.process_request(valid_func=form.process_restict_access_spatially)


@login_required
@check_permission(
    PermissionEnum.CAN_EDIT_METADATA
)
@check_ownership(Metadata, 'metadata_id')
def restore(request: HttpRequest, metadata_id):
    """ Drops custom metadata and load original metadata from capabilities and ISO metadata

    Args,
        request: The incoming request
        id: The metadata id
    Returns:
         Redirects back to edit view
    """
    metadata = get_object_or_404(Metadata,
                                 ~Q(metadata_type=MetadataEnum.CATALOGUE.value),
                                 id=metadata_id)

    form = RestoreMetadataForm(data=request.POST or None,
                               request=request,
                               reverse_lookup='editor:restore',
                               reverse_args=[metadata_id, ],
                               # ToDo: after refactoring of all forms is done, show_modal can be removed
                               show_modal=True,
                               is_confirmed_label=_("Do you really want to restore this metadata?"),
                               form_title=_(f"Restore metadata <strong>{metadata.title}</strong>"),
                               instance=metadata)
    return form.process_request(valid_func=form.process_restore_metadata)


@login_required
@check_permission(
    PermissionEnum.CAN_EDIT_METADATA
)
@check_ownership(Metadata, 'metadata_id')
def restore_dataset_metadata(request: HttpRequest, metadata_id):
    """ Drops custom metadata and load original metadata from capabilities and ISO metadata

    Args,
        request: The incoming request
        metadata_id: The metadata id
    Returns:
         Redirects back to edit view
    """
    metadata = get_object_or_404(Metadata,
                                 ~Q(metadata_type=MetadataEnum.CATALOGUE.value),
                                 id=metadata_id)

    form = RestoreDatasetMetadata(data=request.POST or None,
                                  request=request,
                                  reverse_lookup='editor:restore-dataset-metadata',
                                  reverse_args=[metadata_id, ],
                                  # ToDo: after refactoring of all forms is done, show_modal can be removed
                                  show_modal=True,
                                  is_confirmed_label=_("Do you really want to restore this dataset?"),
                                  form_title=_(f"Restore dataset metadata <strong>{metadata.title}</strong>"),
                                  instance=metadata)
    return form.process_request(valid_func=form.process_restore_dataset_metadata)
