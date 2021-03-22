from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpRequest
from MrMap.icons import get_all_icons
from MrMap.settings import GIT_REPO_URI, GIT_GRAPH_URI
from MrMap.sub_settings.dev_settings import ROOT_URL
from monitoring.models import MonitoringRun
from service.helper.enums import OGCServiceEnum
from service.models import Metadata
from structure.models import PublishRequest, Organization, PendingTask


def default_context(request: HttpRequest):
    mr_map_organization_count = Organization.objects.count()
    mr_map_user_count = get_user_model().objects.count()

    if request.user.is_anonymous:
        pending_publish_requests_count = None
        pending_monitoring_count = None
        pending_tasks_count = None
        wms_count = None
        wfs_count = None
        csw_count = None
        dataset_count = None
    else:
        if not request.user.is_superuser:
            # show only requests for groups or organization where the user is member of
            # superuser can see all pending requests
            pending_publish_requests_count = PublishRequest.objects.filter(Q(group__in=request.user.groups.all()) |
                                                                           Q(organization=request.user.organization)).count()
        else:
            pending_publish_requests_count = PublishRequest.objects.count()

        pending_monitoring_count = MonitoringRun.objects.filter(end=None).count()
        pending_tasks_count = PendingTask.objects.count()

        wms_count = Metadata.objects.filter(service__service_type__name=OGCServiceEnum.WMS.value,
                                            service__is_root=True,
                                            owned_by_org__in=request.user.organization.get_publishable_organizations(),
                                            is_deleted=False,
                                            service__is_update_candidate_for=None,).count()
        wfs_count = Metadata.objects.filter(service__service_type__name=OGCServiceEnum.WFS.value,
                                            owned_by_org__in=request.user.organization.get_publishable_organizations(),
                                            is_deleted=False,
                                            service__is_update_candidate_for=None, ).count()
        csw_count = Metadata.objects.filter(service__service_type__name=OGCServiceEnum.CSW.value,
                                            owned_by_org__in=request.user.organization.get_publishable_organizations(),
                                            is_deleted=False,
                                            service__is_update_candidate_for=None, ).count()
        dataset_count = request.user.get_datasets_as_qs().count()

    return {
        "ROOT_URL": ROOT_URL,
        "PATH": request.path.split("/")[1],
        "FULL_PATH": request.path,
        "LANGUAGE_CODE": request.LANGUAGE_CODE,
        "GIT_REPO_URI": GIT_REPO_URI,
        "GIT_GRAPH_URI": GIT_GRAPH_URI,
        "ICONS": get_all_icons(),
        "mr_map_organization_count": mr_map_organization_count,
        "mr_map_user_count": mr_map_user_count,
        "pending_publish_requests_count": pending_publish_requests_count,
        "pending_monitoring_count": pending_monitoring_count,
        "pending_tasks_count": pending_tasks_count,
        "wms_count": wms_count,
        "wfs_count": wfs_count,
        "csw_count": csw_count,
        "dataset_count": dataset_count,

    }
