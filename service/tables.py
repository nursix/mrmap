import csv

import django_tables2 as tables
from django.shortcuts import render
from django.urls import reverse
from django.utils.html import format_html
from django_bootstrap_swt.components import ProgressBar, Link, Tag, Badge, Accordion
from django_bootstrap_swt.utils import RenderHelper
from django_tables2.export import TableExport

from MrMap.columns import MrMapColumn
from MrMap.icons import IconEnum
from MrMap.tables import MrMapTable
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from csw.models import HarvestResult
from service.helper.enums import MetadataEnum, OGCServiceEnum
from service.models import MetadataRelation, Metadata, FeatureTypeElement, ProxyLog
from structure.models import PendingTask


TOOLTIP_TITLE = _('The resource title')
TOOLTIP_ACTIVE = _('Shows whether the resource is active or not.')
TOOLTIP_SECURED_ACCESS = _('Shows whether the resource is only accessible for certain groups and/or in certain areas.')
TOOLTIP_SECURED_EXTERNALLY = _('Shows whether the resource needs authentication to its origin server.')
TOOLTIP_VERSION = _('The resource version')
TOOLTIP_DATA_PROVIDER = _('The organization which provides the resource.')
TOOLTIP_REGISTERED_BY_GROUP = _('The group which registered the resource.')
TOOLTIP_REGISTERED_FOR = _('The organization for which the resource is registered.')
TOOLTIP_CREATED_ON = _('The registration date.')
TOOLTIP_ACTIONS = _('Performable Actions')
TOOLTIP_STATUS = _(
    'Shows the status of the resource. You can see active state, secured access state and secured externally state.')
TOOLTIP_HEALTH = _('Shows the health status of the resource.')


class PendingTaskTable(tables.Table):
    bs4helper = None
    status = tables.Column(verbose_name=_('Status'),
                           accessor='status_icons',
                           attrs={"th": {"class": "col-sm-1"}})
    service = tables.Column(verbose_name=_('Service'),
                            accessor='service_uri',
                            attrs={"th": {"class": "col-sm-3"}})
    phase = tables.Column(verbose_name=_('Phase'),
                          attrs={"th": {"class": "col-sm-4"}})
    progress = tables.Column(verbose_name=_('Progress'),
                             attrs={"th": {"class": "col-sm-3"}})
    actions = tables.Column(verbose_name=_('Actions'),
                            accessor='action_buttons',
                            attrs={"td": {"style": "white-space:nowrap;"}, "th": {"class": "col-sm-1"}})

    class Meta:
        model = PendingTask
        fields = ('status', 'service', 'phase', 'progress', 'actions')
        template_name = "skeletons/django_tables2_bootstrap4_custom.html"
        prefix = 'pending-task-table'
        orderable = False

    def before_render(self, request):
        self.render_helper = RenderHelper(user_permissions=list(filter(None, request.user.get_permissions())))

    def render_status(self, value):
        return format_html(self.render_helper.render_list_coherent(value))

    def render_actions(self, value):
        self.render_helper.update_attrs = {"class": ["btn-sm"]}
        renderd_actions = self.render_helper.render_list_coherent(items=value)
        self.render_helper.update_attrs = None
        return format_html(renderd_actions)

    @staticmethod
    def render_progress(value):
        return ProgressBar(progress=round(value, 2)).render(safe=True)


class OgcServiceTable(tables.Table):
    bs4helper = None
    layers = tables.Column(verbose_name=_('Layers'), empty_values=[], accessor='service__child_service__count')
    featuretypes = tables.Column(verbose_name=_('Featuretypes'), empty_values=[], accessor='service__featuretypes__count')
    parent_service = tables.Column(verbose_name=_('Parent service'), empty_values=[],
                                   accessor='service__parent_service__metadata')
    status = tables.Column(verbose_name=_('Status'), empty_values=[], )
    health = tables.Column(verbose_name=_('Health'), empty_values=[], )
    last_harvest = tables.Column(verbose_name=_('Last harvest'), empty_values=[], )
    collected_harvest_records = tables.Column(verbose_name=_('Collected harvest records'), empty_values=[], )
    actions = tables.Column(verbose_name=_('Actions'), empty_values=[], orderable=False,
                            attrs={"td": {"style": "white-space:nowrap;"}})

    class Meta:
        model = Metadata
        fields = ('title',
                  'layers',
                  'featuretypes',
                  'parent_service',
                  'status',
                  'health',
                  'service__service_type__version',
                  'last_harvest',
                  'collected_harvest_records',
                  'contact',
                  'service__created_by',
                  'service__published_for',
                  'created',
                  'actions')
        template_name = "skeletons/django_tables2_bootstrap4_custom.html"
        # todo: set this prefix dynamic
        prefix = 'ogc-service-table'

    def before_render(self, request):
        self.render_helper = RenderHelper(user_permissions=list(filter(None, request.user.get_permissions())),
                                          update_url_qs={'current-view': request.resolver_match.view_name})

    def render_title(self, record, value):
        return Link(url=record.detail_view_uri, content=value).render(safe=True)

    def render_last_haverest(self, value):
        harvest_result = HarvestResult.objects.filter(
            service=value
        ).order_by(
            "-created"
        ).first()

        return harvest_result.timestamp_start if harvest_result is not None else None

    def render_collected_haverest_records(self, value):
        harvest_result = HarvestResult.objects.filter(
            service=value
        ).order_by(
            "-created"
        ).first()
        return harvest_result.number_results if harvest_result is not None else None

    def render_parent_service(self, value):
        return Link(url=value.detail_view_uri, content=value).render(safe=True)

    def render_status(self, record):
        return format_html(self.render_helper.render_list_coherent(items=record.get_status_icons(), safe=True))

    def render_health(self, record):
        return format_html(self.render_helper.render_list_coherent(items=record.get_health_icons(), safe=True))

    def render_contact(self, value):
        return Link(url=value.detail_view_uri, content=value).render(safe=True)

    def render_service__created_by(self, value):
        return Link(url=value.detail_view_uri, content=value).render(safe=True)

    def render_service__published_for(self, value):
        return Link(url=value.detail_view_uri, content=value).render(safe=True)

    def render_actions(self, record):
        self.render_helper.update_attrs = {"class": ["btn-sm", "mr-1"]}
        renderd_actions = self.render_helper.render_list_coherent(items=record.get_actions())
        self.render_helper.update_attrs = None
        return format_html(renderd_actions)

    def order_layers(self, queryset, is_descending):
        queryset = queryset.annotate(
            count=Count("service__child_service")
        ).order_by(("-" if is_descending else "") + "count")
        return queryset, True

    def order_wfs_featuretypes(self, queryset, is_descending):
        queryset = queryset.annotate(
            count=Count("service__featuretypes")
        ).order_by(("-" if is_descending else "") + "count")
        return queryset, True

    def order_status(self, queryset, is_descending):
        is_descending_str = "-" if is_descending else ""
        queryset = queryset.order_by(is_descending_str + "is_active",
                                     is_descending_str + "is_secured",
                                     is_descending_str + "external_authentication", )
        return queryset, True

    def order_health(self, queryset, is_descending):
        # TODO:
        return queryset, True


class DatasetTable(tables.Table):
    bs4helper = None
    related_objects = MrMapColumn(verbose_name=_('Related objects'), empty_values=[])
    origins = MrMapColumn(verbose_name=_('Origins'), empty_values=[])
    actions = tables.Column(verbose_name=_('Actions'), empty_values=[], orderable=False,
                            attrs={"td": {"style": "white-space:nowrap;"}})

    class Meta:
        model = Metadata
        fields = (
                  'title',
                  'related_objects',
                  'origins',
                  'actions')
        template_name = "skeletons/django_tables2_bootstrap4_custom.html"
        # todo: set this prefix dynamic
        prefix = 'wms-table'

    def before_render(self, request):
        self.render_helper = RenderHelper(user_permissions=list(filter(None, request.user.get_permissions())))

    def render_title(self, value, record):
        return Link(url=record.detail_html_view_uri, content=value, open_in_new_tab=True).render(safe=True)

    def render_related_objects(self, record):
        related_metadatas = Metadata.objects.filter(
            related_metadata__metadata_to=record
        ).prefetch_related(
            "related_metadata"
        )
        link_list = []
        for metadata in related_metadatas:
            if metadata.metadata_type == MetadataEnum.FEATURETYPE.value:
                kind_of_resource_icon = IconEnum.FEATURETYPE.value
                kind_of_resource = "Featuretype"
            elif metadata.metadata_type == MetadataEnum.LAYER.value:
                kind_of_resource_icon = IconEnum.LAYER.value
                kind_of_resource = "Layer"
            else:
                kind_of_resource_icon = ""
                kind_of_resource = ""
            kind_of_resource_icon = Tag(tag='i', attrs={"class": [kind_of_resource_icon]}, ).render()

            link_list.append(Link(url=metadata.detail_view_uri,
                                  content=format_html(kind_of_resource_icon + f" {metadata.title} [{metadata.id}]"),
                                  tooltip=_(f'Click to open the detail view of related {kind_of_resource} <strong>{metadata.title} [{metadata.id}]"</strong>'),), )
        return format_html(self.render_helper.render_list_coherent(items=link_list))

    def render_origins(self, record):
        related_metadatas = MetadataRelation.objects.filter(
            metadata_to=record
        )
        origin_list = []
        rel_mds = list(record.related_metadata.all())
        relations = list(related_metadatas) + rel_mds
        for relation in relations:
            origin_list.append(f"{relation.origin}")

        return format_html(', '.join(origin_list))

    def render_actions(self, record):
        self.render_helper.update_attrs = {"class": ["btn-sm", "mr-1"]}
        renderd_actions = self.render_helper.render_list_coherent(items=record.get_actions())
        self.render_helper.update_attrs = None
        return format_html(renderd_actions)


class FeatureTypeElementTable(tables.Table):
    class Meta:
        model = FeatureTypeElement
        fields = ('name', 'type', )


class ResourceDetailTable(tables.Table):
    bs4helper = None
    parent_service = tables.Column(verbose_name=_('Parent service'))
    bbox_lat_lon = tables.Column(verbose_name=_('Bbox lat lon'))
    scale_min_max = tables.Column(verbose_name=_('Scale range'), empty_values=[])
    mime_types = tables.Column(verbose_name=_('Mime types'), empty_values=[], attrs={'td': {'class': 'col-sm-10'}})

    class Meta:
        model = Metadata
        fields = ('public_id',
                  'service__service_type__name',
                  'service__service_type__version',
                  'last_modified',
                  'service__layer__identifier',
                  'parent_service',
                  'contact__person_name',
                  'contact__organization_name',
                  'contact__phone',
                  'contact__facsimile',
                  'contact__email',
                  'contact__address',
                  'contact__city',
                  'contact__postal_code',
                  'contact__state_or_province',
                  'contact__country',
                  'title',
                  'abstract',
                  'online_resource',
                  'keywords__all',
                  'access_constraints',
                  'service__layer__is_available',
                  'service__layer__is_queryable',
                  'service__layer__is_opaque',
                  'service__layer__is_cascaded',
                  'featuretype__is_searchable',
                  'is_secured',
                  'hits',
                  'scale_min_max',
                  'bbox_lat_lon',
                  'featuretype__default_srs',
                  'reference_system__all',
                  'mime_types',
                  )
        template_name = "skeletons/django_tables2_vertical_table.html"
        # todo: set this prefix dynamic
        prefix = 'layer-detail-table'
        orderable = False

    def __init__(self, *args, **kwargs):
        super(ResourceDetailTable, self).__init__(*args, **kwargs)
        self.exclude = []
        if self.data[0].is_metadata_type(MetadataEnum.SERVICE):
            self.exclude.extend(['parent_service',
                                 'service__layer__identifier',
                                 'service__layer__is_available',
                                 'service__layer__is_queryable',
                                 'service__layer__is_opaque',
                                 'service__layer__is_cascaded',
                                 'scale_min_max',
                                 'bbox_lat_lon',
                                 'featuretype__default_srs', ])
            if self.data[0].is_service_type(OGCServiceEnum.WFS):
                self.exclude.extend(['featuretype__is_searchable', ])
        else:
            self.exclude.extend([
                'access_constraints',
                'service__service_type__name',
                'service__service_type__version',
                'last_modified',
                'online_resource',
                'contact__person_name',
                'contact__organization_name',
                'contact__phone',
                'contact__facsimile',
                'contact__email',
                'contact__address',
                'contact__city',
                'contact__postal_code',
                'contact__state_or_province',
                'contact__country',
            ])

            if self.data[0].is_metadata_type(MetadataEnum.FEATURETYPE):
                self.exclude.extend(['service__layer__identifier',
                                     'service__layer__is_available',
                                     'service__layer__is_queryable',
                                     'service__layer__is_opaque',
                                     'service__layer__is_cascaded',
                                     'scale_min_max', ])

                self.columns['parent_service'].column.accessor = 'featuretype__parent_service__metadata'
                self.columns['bbox_lat_lon'].column.accessor = 'featuretype__bbox_lat_lon'
            else:
                self.exclude.extend(['featuretype__default_srs', ])
                self.columns['parent_service'].column.accessor = 'service__parent_service__metadata'
                self.columns['bbox_lat_lon'].column.accessor = 'service__layer__bbox_lat_lon'

    def render_parent_service(self, value):
        return Link(url=value.detail_view_uri, content=value).render(safe=True)

    def render_online_resource(self, value):
        return Link(url=value, content=value).render(safe=True)

    def render_keywords__all(self, value):
        badges = ''
        for kw in value:
            badges += Badge(content=kw, badge_pill=True)
        return format_html(badges) if value else _('No keywords provided')

    def render_scale_min_max(self, record):
        return f'[{record.service.layer.scale_min}, {record.service.layer.scale_max}]'

    def render_bbox_lat_lon(self, value):
        if value.area > 0.0:
            return None # LeafletClient(polygon=value).render(safe=True)
        else:
            return _('No spatial data provided!')

    def render_featuretype__default_srs(self, value):
        badge = Badge(content=f'{value.prefix}:{value.code}', badge_pill=True).render(safe=True)
        return badge if value else _('No default reference system provided')

    def render_reference_system__all(self, value):
        badges = ''
        for kw in value:
            badges += Badge(content=f'{kw.prefix}:{kw.code}', badge_pill=True)
        return format_html(badges) if value else _('No additional reference systems provided')

    def render_mime_types(self, record):
        mime_types = {}
        formats = record.get_formats()
        for mime in formats:
            op = mime_types.get(mime.operation)
            if op is None:
                op = []
            op.append(mime.mime_type)
            mi = {mime.operation: op}
            mime_types.update(mi)
        mime_type_accordions = ''
        for key, values in mime_types.items():
            badges = ''
            for value in values:
                badges += Badge(content=value)
            mime_type_accordions += Accordion(btn_value=key, content=badges)
        return format_html(mime_type_accordions)


class ChildLayerTable(MrMapTable):
    id = tables.Column(visible=False)
    title = tables.Column(visible=False)
    child_layer_title = tables.Column(empty_values=[], order_by='title', )

    caption = _("Shows all child layer of current WMS.")

    @staticmethod
    def render_child_layer_title(record):
        url = reverse('resource:get-metadata-html', args=(record['id'],))

        if record['sublayers_count'] > 0:
            return format_html("<a href='{}'>{} <span class='badge badge-secondary'>{}</span></a>",
                               url,
                               record['title'],
                               record['sublayers_count'])
        else:
            return format_html("<a href='{}'>{}</a>",
                               url,
                               record['title'], )


class FeatureTypeTable(MrMapTable):
    id = tables.Column(visible=False)
    title = tables.Column(visible=False)
    featuretype_title = tables.Column(empty_values=[], order_by='title', )

    caption = _("Shows all featuretypes of current WFS.")

    @staticmethod
    def render_featuretype_title(record):
        url = reverse('resource:get-metadata-html', args=(record['id'],))

        return format_html("<a href='{}'>{}</a>",
                           url,
                           record['title'], )


class CoupledMetadataTable(MrMapTable):
    id = tables.Column(visible=False)
    title = tables.Column(visible=False)
    coupled_metadata_title = tables.Column(empty_values=[], order_by='title', )

    caption = _("Shows all coupled metadata of current service.")

    @staticmethod
    def render_coupled_metadata_title(record):
        url = reverse('resource:get-metadata-html', args=(record['id'],))

        return format_html("<a href='{}'>{}</a>",
                           url,
                           record['title'], )


class UpdateServiceElements(MrMapTable):
    title = tables.Column(empty_values=[], )
    identifier = tables.Column(empty_values=[], )


class ProxyLogTable(tables.Table):
    caption = _("Shows all logs for a service.")
    user = tables.Column(default='Public group')

    class Meta:
        model = ProxyLog
        fields = ('metadata__id', 'metadata__title', 'timestamp', 'operation', 'response_wms_megapixel', 'response_wfs_num_features')
        sequence = ('metadata__id', 'metadata__title', 'user', '...')
        template_name = "skeletons/django_tables2_bootstrap4_custom.html"
        prefix = 'proxy-log-table'

    def fill_csv_response(self, stream):
        csv_writer = csv.writer(stream)
        csv_writer.writerow([
            _("ID"),
            _("Title"),
            _("User"),
            _("Operation"),
            _("Delivered Features (WFS)"),
            _("Delivered Megapixel (WMS)"),
            _("Timestamp"),
        ])
        for log in self.data.data:
            csv_writer.writerow(
                [
                    log.metadata.id,
                    log.metadata.title,
                    log.user,
                    log.operation,
                    log.response_wfs_num_features,
                    log.response_wms_megapixel,
                    log.timestamp,
                ]
            )
        return stream.getvalue()


