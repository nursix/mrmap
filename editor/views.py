import json

from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Case, When
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from MrMap import utils
from MrMap.cacher import PageCacher
from MrMap.decorator import check_permission, check_ownership
from MrMap.forms import MrMapConfirmForm
from MrMap.messages import METADATA_RESTORING_SUCCESS, METADATA_EDITING_SUCCESS, \
    METADATA_IS_ORIGINAL, SERVICE_MD_RESTORED, SERVICE_MD_EDITED, NO_PERMISSION, EDITOR_ACCESS_RESTRICTED, \
    SECURITY_PROXY_WARNING_ONLY_FOR_ROOT
from MrMap.responses import DefaultContext, BackendAjaxResponse
from api.settings import API_CACHE_KEY_PREFIX
from editor.forms import MetadataEditorForm
from editor.settings import WMS_SECURED_OPERATIONS, WFS_SECURED_OPERATIONS
from editor.wizards import DATASET_WIZARD_FORMS, DatasetWizard
from service.filters import MetadataWmsFilter, MetadataWfsFilter, MetadataDatasetFilter
from service.helper.enums import OGCServiceEnum, MetadataEnum
from service.models import RequestOperation, SecuredOperation, Metadata
from service.tasks import async_process_secure_operations_form
from structure.models import MrMapUser, Permission, MrMapGroup
from users.helper import user_helper
from editor.helper import editor_helper
from editor.tables import *


def _prepare_wms_table(request: HttpRequest, user: MrMapUser, current_view: str):
    return WmsServiceTable(request=request,
                           filter_set_class=MetadataWmsFilter,
                           queryset=user.get_services_as_qs(OGCServiceEnum.WMS),
                           current_view=current_view,
                           param_lead='wms-t',)


def _prepare_wfs_table(request: HttpRequest, user: MrMapUser, current_view: str):
    return WfsServiceTable(request=request,
                           filter_set_class=MetadataWfsFilter,
                           queryset=user.get_services_as_qs(OGCServiceEnum.WFS),
                           current_view=current_view,
                           param_lead='wfs-t', )


def _prepare_dataset_table(request: HttpRequest, user: MrMapUser, current_view: str):
    return DatasetTable(request=request,
                        filter_set_class=MetadataDatasetFilter,
                        queryset=user.get_datasets_as_qs(),
                        current_view=current_view,
                        param_lead='dataset-t',)


@login_required
@check_permission(Permission(can_edit_metadata_service=True))
def index(request: HttpRequest, update_params: dict = None, status_code: int = 200, ):
    """ The index view of the editor app.

    Lists all services with information of custom set metadata.

    Args:
        request: The incoming request

    Returns:
    """
    user = user_helper.get_user(request)
    template = "views/editor_service_table_index.html"

    params = {
        "wms_table": _prepare_wms_table(request=request, user=user, current_view='editor:index'),
        "wfs_table": _prepare_wfs_table(request=request, user=user, current_view='editor:index'),
        "dataset_table": _prepare_dataset_table(request=request, user=user, current_view='editor:index'),
        "current_view": 'editor:index',
    }
    if update_params:
        params.update(update_params)

    context = DefaultContext(request, params, user)
    return render(request=request, template_name=template, context=context.get_context(), status=status_code)


@login_required
@check_permission(Permission(can_edit_metadata_service=True))
def index_wms(request: HttpRequest, update_params=None, status_code: int = 200, ):
    """ The index view of the editor app.

    Lists all services with information of custom set metadata.

    Args:
        request: The incoming request
    Returns:
    """
    user = user_helper.get_user(request)

    template = "views/editor_service_table_index_wms.html"

    params = {
        "wms_table": _prepare_wms_table(request=request, user=user, current_view='editor:wms-index'),
        "current_view": "editr:wms-index"
    }
    if update_params:
        params.update(update_params)

    context = DefaultContext(request, params, user)
    return render(request=request, template_name=template, context=context.get_context(), status=status_code)


@login_required
@check_permission(Permission(can_edit_metadata_service=True))
def index_wfs(request: HttpRequest, update_params=None, status_code: int = 200, ):
    """ The index view of the editor app.

    Lists all services with information of custom set metadata.

    Args:
        request: The incoming request
    Returns:
    """
    user = user_helper.get_user(request)

    template = "views/editor_service_table_index_wfs.html"

    params = {
        "wfs_table": _prepare_wfs_table(request=request, user=user, current_view='editor:wfs-index'),
        "current_view": "editor:wfs-index"
    }
    if update_params:
        params.update(update_params)

    context = DefaultContext(request, params, user)
    return render(request=request, template_name=template, context=context.get_context(), status=status_code)


@login_required
@check_permission(Permission(can_edit_metadata_service=True))
def index_datasets(request: HttpRequest, update_params=None, status_code: int = 200, ):
    """ The index view of the editor app.

    Lists all datasets with information of custom set metadata.

    Args:
        request: The incoming request
        update_params:
        status_code:
    Returns:
    """
    user = user_helper.get_user(request)

    template = "views/editor_service_table_index_datasets.html"

    params = {
        "dataset_table": _prepare_dataset_table(request=request, user=user, current_view='editor:datasets-index'),
        "current_view": 'editor:datasets-index',
    }

    if update_params:
        params.update(update_params)

    context = DefaultContext(request, params, user)
    return render(request=request,
                  template_name=template,
                  context=context.get_context(),
                  status=status_code)


"""
    Post views below
"""


@login_required
@check_permission(Permission(can_remove_dataset_metadata=True))
@check_ownership(Metadata, 'metadata_id')
def remove_dataset(request: HttpRequest, metadata_id: int, current_view: str):
    """ The remove view for dataset metadata

    Args:
        request: The incoming request
        metadata_id: The metadata id
    Returns:
        A rendered view
    """
    metadata = get_object_or_404(Metadata, id=metadata_id)
    if metadata.metadata_type.type != 'dataset':
        messages.success(request, message=_("You can't delete metadata record"))
        return HttpResponseRedirect(reverse(current_view, ), status=303)

    relations = MetadataRelation.objects.filter(metadata_to=metadata)
    is_mr_map_origin = True
    for relation in relations:
        if relation.origin.name != "MrMap":
            is_mr_map_origin = False
            break
    if is_mr_map_origin is not True:
        messages.success(request, message=_("You can't delete autogenerated datasets"))
        return HttpResponseRedirect(reverse(current_view, ), status=303)

    form = MrMapConfirmForm(data=request.POST or None,
                            request=request,
                            current_view=current_view,
                            reverse_lookup='editor:remove-dataset-metadata',
                            reverse_args=[metadata_id, current_view],
                            # ToDo: after refactoring of all forms is done, show_modal can be removed
                            show_modal=True,
                            is_confirmed_label=_("Do you really want to delete this dataset?"),
                            )

    if request.method == 'GET':
        return form.render_view()

    if request.method == 'POST':
        if form.is_valid():
            metadata.delete(force=True)
            messages.success(request, message=_("Dataset successfully deleted."))
            return HttpResponseRedirect(reverse(current_view, ), status=303)
        else:
            form.fade_modal = False
            return form.render_view(status_code=422)
    else:
        return HttpResponseRedirect(reverse(current_view, ), status=303)


@login_required
@check_permission(Permission(can_add_dataset_metadata=True))
def add_new_dataset_wizard(request: HttpRequest, current_view: str):
    return DatasetWizard.as_view(form_list=DATASET_WIZARD_FORMS,
                                 ignore_uncomitted_forms=True,
                                 current_view=current_view,
                                 title=_(format_html('<b>Add New Dataset</b>')),
                                 id_wizard='add_new_dataset_wizard',
                                 )(request=request)


@login_required
@check_permission(Permission(can_edit_dataset_metadata=True))
@check_ownership(Metadata, 'metadata_id')
def edit_dataset_wizard(request, current_view: str, metadata_id: int):
    metadata = get_object_or_404(Metadata, id=metadata_id)
    return DatasetWizard.as_view(form_list=DATASET_WIZARD_FORMS,
                                 ignore_uncomitted_forms=True,
                                 current_view=current_view,
                                 instance_id=metadata_id,
                                 title=_(format_html(f'<b>Edit</b> <i>{metadata.title}</i> <b>Dataset</b>')),
                                 id_wizard=f'edit_{metadata.id}_dataset_wizard',
                                 )(request=request)


@login_required
@check_permission(Permission(can_edit_metadata_service=True))
@check_ownership(Metadata, 'metadata_id')
def edit(request: HttpRequest, metadata_id: int, current_view: str):
    """ The edit view for metadata

    Provides editing functions for all elements which are described by Metadata objects

    Args:
        request: The incoming request
        metadata_id: The metadata id
    Returns:
        A rendered view
    """
    user = user_helper.get_user(request)

    metadata = get_object_or_404(Metadata, id=metadata_id)
    if metadata.metadata_type.type == 'dataset':
        return HttpResponseRedirect(reverse("editor:edit-dataset-metadata", args=(metadata_id,)), status=303)

    form = MetadataEditorForm(data=request.POST or None,
                              instance=metadata,
                              request=request,
                              current_view=current_view,
                              reverse_lookup='editor:edit',
                              reverse_args=[metadata_id, current_view],
                              # ToDo: after refactoring of all forms is done, show_modal can be removed
                              show_modal=True,
                              has_autocomplete_fields=True,
                              form_title=_(f"Edit metadata <strong>{metadata.title}</strong>")
                              )

    if request.method == 'GET':
        return form.render_view()

    if request.method == 'POST':
        if form.is_valid():
            custom_md = form.save(commit=False)
            if not metadata.is_root():
                # this is for the case that we are working on a non root element which is not allowed to change the
                # inheritance setting for the whole service -> we act like it didn't change
                custom_md.use_proxy_uri = metadata.use_proxy_uri

                # Furthermore we remove a possibly existing current_capability_document for this element, since the metadata
                # might have changed!
                metadata.clear_cached_documents()

            editor_helper.resolve_iso_metadata_links(request, metadata, form)
            editor_helper.overwrite_metadata(metadata, custom_md, form)

            # Clear page cache for API, so the changes will be visible on the next cache
            p_cacher = PageCacher()
            p_cacher.remove_pages(API_CACHE_KEY_PREFIX)

            messages.add_message(request, messages.SUCCESS, METADATA_EDITING_SUCCESS)

            if metadata.is_root():
                parent_service = metadata.service
            else:
                if metadata.is_service_type(OGCServiceEnum.WMS):
                    parent_service = metadata.service.parent_service
                elif metadata.is_service_type(OGCServiceEnum.WFS):
                    parent_service = metadata.featuretype.parent_service

            user_helper.create_group_activity(metadata.created_by, user, SERVICE_MD_EDITED,
                                              "{}: {}".format(parent_service.metadata.title, metadata.title))
            return HttpResponseRedirect(reverse(current_view, ), status=303)
        else:
            form.fade_modal = False
            form.render_view(status_code=422)

    return HttpResponseRedirect(reverse(current_view, ), status=303)


@login_required
@check_permission(Permission(can_edit_metadata_service=True))
@check_ownership(Metadata, 'id')
def edit_access(request: HttpRequest, id: int):
    """ The edit view for the operations access

    Provides a form to set the access permissions for a metadata-related object.
    Processes the form input afterwards

    Args:
        request (HttpRequest): The incoming request
        id (int): The metadata id
    Returns:
         A rendered view
    """
    user = user_helper.get_user(request)

    md = Metadata.objects.get(id=id)
    template = "views/editor_edit_access_index.html"
    post_params = request.POST

    if request.method == "POST":
        # process form input using async tasks
        try:
            async_process_secure_operations_form.delay(post_params, md.id)
        except Exception as e:
            messages.error(request, message=e)
            return redirect("editor:edit_access", md.id)
        messages.success(request, EDITOR_ACCESS_RESTRICTED.format(md.title))
        md.save()
        if md.is_metadata_type(MetadataEnum.FEATURETYPE):
            redirect_id = md.featuretype.parent_service.metadata.id
        else:
            if md.service.is_root:
                redirect_id = md.id
            else:
                redirect_id = md.service.parent_service.metadata.id
        return redirect("service:detail", redirect_id)

    else:
        # render form
        secured_operations = []
        if md.is_service_type(OGCServiceEnum.WMS):
            secured_operations = WMS_SECURED_OPERATIONS
        elif md.is_service_type(OGCServiceEnum.WFS):
            secured_operations = WFS_SECURED_OPERATIONS

        operations = RequestOperation.objects.filter(
            operation_name__in=secured_operations
        )
        sec_ops = SecuredOperation.objects.filter(
            secured_metadata=md
        )
        all_groups = MrMapGroup.objects.all().order_by(Case(When(name='Public', then=0)), 'name')
        tmp = editor_helper.prepare_secured_operations_groups(operations, sec_ops, all_groups, md)

        spatial_restrictable_operations = [
            "GetMap",  # WMS
            "GetFeature"  # WFS
        ]

        params = {
            "service_metadata": md,
            "has_ext_auth": md.has_external_authentication(),
            "operations": tmp,
            "spatial_restrictable_operations": spatial_restrictable_operations,
        }

    context = DefaultContext(request, params, user).get_context()
    return render(request, template, context)


@login_required
def access_geometry_form(request: HttpRequest, id: int):
    """ Renders the geometry form for the access editing

    Args:
        request (HttpRequest): The incoming request
        id (int): The id of the metadata object, which will be edited
    Returns:
         BackendAjaxResponse
    """

    user = user_helper.get_user(request)
    template = "views/access_geometry_form.html"

    GET_params = request.GET
    operation = GET_params.get("operation", None)
    group_id = GET_params.get("groupId", None)
    polygons = utils.resolve_none_string(GET_params.get("polygons", 'None'))

    if polygons is not None:
        polygons = json.loads(polygons)
        if not isinstance(polygons, list):
            polygons = [polygons]

    md = Metadata.objects.get(id=id)

    if not md.is_root():
        messages.info(request, message=SECURITY_PROXY_WARNING_ONLY_FOR_ROOT)
        return BackendAjaxResponse(html="", redirect=reverse('edit_access', args=(md.id,))).get_response()

    service_bounding_geometry = md.find_max_bounding_box()

    params = {
        "action_url": reverse('editor:access_geometry_form', args=(md.id,)),
        "bbox": service_bounding_geometry,
        "group_id": group_id,
        "operation": operation,
        "polygons": polygons,
    }
    context = DefaultContext(request, params, user).get_context()
    html = render_to_string(template_name=template, request=request, context=context)
    return BackendAjaxResponse(html=html).get_response()


@login_required
@check_permission(Permission(can_edit_metadata_service=True))
@check_ownership(Metadata, 'metadata_id')
def restore(request: HttpRequest, metadata_id: int, current_view: str):
    """ Drops custom metadata and load original metadata from capabilities and ISO metadata

    Args,
        request: The incoming request
        id: The metadata id
    Returns:
         Redirects back to edit view
    """
    user = user_helper.get_user(request)

    metadata = Metadata.objects.get(id=metadata_id)

    form = MrMapConfirmForm(data=request.POST or None,
                            request=request,
                            current_view=current_view,
                            reverse_lookup='editor:restore',
                            reverse_args=[metadata_id, current_view],
                            # ToDo: after refactoring of all forms is done, show_modal can be removed
                            show_modal=True,
                            is_confirmed_label=_("Do you really want to restore this dataset?"),
                            form_title=_(f"Restore metadata <strong>{metadata.title}</strong>")
                            )

    if request.method == 'GET':
        return form.render_view()

    if request.method == 'POST':
        if form.is_valid():
            ext_auth = metadata.get_external_authentication_object()
            service_type = metadata.get_service_type()
            if service_type == 'wms':
                children_md = Metadata.objects.filter(service__parent_service__metadata=metadata, is_custom=True)
            elif service_type == 'wfs':
                children_md = Metadata.objects.filter(featuretype__parent_service__metadata=metadata, is_custom=True)

            if not metadata.is_custom and len(children_md) == 0:
                messages.add_message(request, messages.INFO, METADATA_IS_ORIGINAL)
                return HttpResponseRedirect(reverse(current_view), status=303)

            if metadata.is_custom:
                metadata.restore(metadata.identifier, external_auth=ext_auth)
                metadata.save()

            for md in children_md:
                md.restore(md.identifier)
                md.save()
            messages.add_message(request, messages.SUCCESS, METADATA_RESTORING_SUCCESS)
            if not metadata.is_root():
                if service_type == 'wms':
                    parent_metadata = metadata.service.parent_service.metadata
                elif service_type == 'wfs':
                    parent_metadata = metadata.featuretype.parent_service.metadata
                else:
                    # This case is not important now
                    pass
            else:
                parent_metadata = metadata
            user_helper.create_group_activity(metadata.created_by, user, SERVICE_MD_RESTORED,
                                              "{}: {}".format(parent_metadata.title, metadata.title))

            return HttpResponseRedirect(reverse(current_view), status=303)
        else:
            form.fade_modal = False
            return form.render_view(status_code=422)
    else:
        return HttpResponseRedirect(reverse(current_view), status=303)


@login_required
@check_permission(Permission(can_edit_metadata_service=True))
@check_ownership(Metadata, 'metadata_id')
def restore_dataset_metadata(request: HttpRequest, metadata_id: int, current_view: str):
    """ Drops custom metadata and load original metadata from capabilities and ISO metadata

    Args,
        request: The incoming request
        id: The metadata id
    Returns:
         Redirects back to edit view
    """
    user = user_helper.get_user(request)

    metadata = get_object_or_404(Metadata, id=metadata_id)
    ext_auth = metadata.get_external_authentication_object()

    form = MrMapConfirmForm(data=request.POST or None,
                            request=request,
                            current_view=current_view,
                            reverse_lookup='editor:restore-dataset-metadata',
                            reverse_args=[metadata_id, current_view],
                            # ToDo: after refactoring of all forms is done, show_modal can be removed
                            show_modal=True,
                            is_confirmed_label=_("Do you really want to restore this dataset?"),
                            form_title=_(f"Restore dataset metadata <strong>{metadata.title}</strong>")
                            )

    if request.method == 'GET':
        return form.render_view()

    if request.method == 'POST':
        if form.is_valid():
            if not metadata.is_custom:
                messages.add_message(request, messages.INFO, METADATA_IS_ORIGINAL)
                return HttpResponseRedirect(reverse(current_view), status=303)

            if metadata.is_custom:
                metadata.restore(metadata.identifier, external_auth=ext_auth)
                metadata.save()

            messages.add_message(request, messages.SUCCESS, METADATA_RESTORING_SUCCESS)
            user_helper.create_group_activity(metadata.created_by, user, SERVICE_MD_RESTORED,
                                              "{}".format(metadata.title, ))
            return HttpResponseRedirect(reverse(current_view), status=303)
        else:
            form.fade_modal = False
            return form.render_view()
    else:
        return HttpResponseRedirect(reverse(current_view), status=303)
