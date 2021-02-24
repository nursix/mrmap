# Generated by Django 3.1.7 on 2021-02-22 14:11

import MrMap.validators
import django.contrib.gis.db.models.fields
import django.contrib.gis.geos.polygon
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllowedOperation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('allowed_area', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326, validators=[MrMap.validators.geometry_is_empty])),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('public_id', models.CharField(blank=True, max_length=255, null=True, unique=True, validators=[MrMap.validators.not_uuid])),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('last_modified', models.DateTimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('type', models.CharField(choices=[(None, '---'), ('iso', 'iso'), ('inspire', 'inspire')], max_length=255)),
                ('title_locale_1', models.CharField(max_length=255, null=True)),
                ('title_locale_2', models.CharField(max_length=255, null=True)),
                ('title_EN', models.CharField(max_length=255, null=True)),
                ('description_locale_1', models.TextField(null=True)),
                ('description_locale_2', models.TextField(null=True)),
                ('description_EN', models.TextField(null=True)),
                ('symbol', models.CharField(max_length=500, null=True)),
                ('online_link', models.CharField(max_length=500, null=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('public_id', models.CharField(blank=True, max_length=255, null=True, unique=True, validators=[MrMap.validators.not_uuid])),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('last_modified', models.DateTimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('language_code', models.CharField(blank=True, max_length=100, null=True)),
                ('language_code_list_url', models.CharField(blank=True, default='https://standards.iso.org/iso/19139/Schemas/resources/codelist/ML_gmxCodelists.xml', max_length=1000, null=True)),
                ('character_set_code', models.CharField(choices=[('utf8', 'utf8'), ('utf16', 'utf16')], default='utf8', max_length=255)),
                ('character_set_code_list_url', models.CharField(blank=True, default='https://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml', max_length=1000, null=True)),
                ('hierarchy_level_code', models.CharField(blank=True, max_length=100, null=True)),
                ('hierarchy_level_code_list_url', models.CharField(blank=True, default='https://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml', max_length=1000, null=True)),
                ('update_frequency_code', models.CharField(blank=True, choices=[('annually', 'annually'), ('asNeeded', 'asNeeded'), ('biannually', 'biannually'), ('irregular', 'irregular'), ('notPlanned', 'notPlanned'), ('unknown', 'unknown')], max_length=255, null=True)),
                ('update_frequency_code_list_url', models.CharField(blank=True, default='https://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml', max_length=1000, null=True)),
                ('legal_restriction_code', models.CharField(blank=True, choices=[('copyright', 'copyright'), ('intellectualPropertyRights', 'intellectualPropertyRights'), ('license', 'license'), ('otherRestrictions', 'otherRestrictions'), ('patent', 'patent'), ('patentPending', 'patentPending'), ('restricted', 'restricted'), ('trademark', 'trademark')], max_length=255, null=True)),
                ('legal_restriction_code_list_url', models.CharField(blank=True, default='https://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml', max_length=1000, null=True)),
                ('legal_restriction_other_constraints', models.TextField(blank=True, null=True)),
                ('date_stamp', models.DateField(blank=True, null=True)),
                ('metadata_standard_name', models.CharField(blank=True, max_length=255, null=True)),
                ('metadata_standard_version', models.CharField(blank=True, max_length=255, null=True)),
                ('md_identifier_code', models.CharField(blank=True, max_length=500, null=True)),
                ('use_limitation', models.TextField(blank=True, null=True)),
                ('distribution_function_code', models.CharField(choices=[('download', 'download'), ('information', 'information'), ('offlineAccess', 'offlineAccess'), ('order', 'order'), ('search', 'search')], default='dataset', max_length=255)),
                ('distribution_function_code_list_url', models.CharField(blank=True, default='https://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml', max_length=1000, null=True)),
                ('lineage_statement', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Dimension',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, choices=[('time', 'time'), ('elevation', 'elevation'), ('other', 'other')], max_length=255, null=True)),
                ('units', models.CharField(blank=True, max_length=255, null=True)),
                ('extent', models.TextField(blank=True, null=True)),
                ('custom_name', models.CharField(blank=True, max_length=500, null=True)),
                ('time_extent_min', models.DateTimeField(blank=True, null=True)),
                ('time_extent_max', models.DateTimeField(blank=True, null=True)),
                ('elev_extent_min', models.FloatField(blank=True, max_length=500, null=True)),
                ('elev_extent_max', models.FloatField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('public_id', models.CharField(blank=True, max_length=255, null=True, unique=True, validators=[MrMap.validators.not_uuid])),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('last_modified', models.DateTimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('document_type', models.CharField(choices=[(None, '---'), ('Capability', 'Capability'), ('Metadata', 'Metadata')], max_length=255, null=True, validators=[MrMap.validators.validate_document_enum_choices])),
                ('content', models.TextField(blank=True, null=True)),
                ('is_original', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ExternalAuthentication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=500)),
                ('auth_type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='FeatureType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('public_id', models.CharField(blank=True, max_length=255, null=True, unique=True, validators=[MrMap.validators.not_uuid])),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('last_modified', models.DateTimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_searchable', models.BooleanField(default=False)),
                ('inspire_download', models.BooleanField(default=False)),
                ('bbox_lat_lon', django.contrib.gis.db.models.fields.PolygonField(default=django.contrib.gis.geos.polygon.Polygon(((-90.0, -180.0), (-90.0, 180.0), (90.0, 180.0), (90.0, -180.0), (-90.0, -180.0))), srid=4326)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FeatureTypeElement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('public_id', models.CharField(blank=True, max_length=255, null=True, unique=True, validators=[MrMap.validators.not_uuid])),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('last_modified', models.DateTimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GenericUrl',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('public_id', models.CharField(blank=True, max_length=255, null=True, unique=True, validators=[MrMap.validators.not_uuid])),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('last_modified', models.DateTimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True, null=True)),
                ('method', models.CharField(blank=True, choices=[(None, '---'), ('Get', 'Get'), ('Post', 'Post')], max_length=255, null=True)),
                ('url', models.URLField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='LegalDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('date_type_code', models.CharField(choices=[('creation', 'creation'), ('publication', 'publication'), ('revision', 'revision')], max_length=255)),
                ('date_type_code_list_url', models.CharField(default='https://standards.iso.org/iso/19139/resources/gmxCodelists.xml', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='LegalReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('explanation', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Licence',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('public_id', models.CharField(blank=True, max_length=255, null=True, unique=True, validators=[MrMap.validators.not_uuid])),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('last_modified', models.DateTimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('identifier', models.CharField(max_length=255, unique=True)),
                ('symbol_url', models.URLField(null=True)),
                ('description', models.TextField()),
                ('description_url', models.URLField(null=True)),
                ('is_open_data', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Metadata',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('public_id', models.CharField(blank=True, max_length=255, null=True, unique=True, validators=[MrMap.validators.not_uuid])),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('last_modified', models.DateTimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('identifier', models.CharField(max_length=1000, null=True)),
                ('title', models.CharField(max_length=1000, verbose_name='Title')),
                ('abstract', models.TextField(blank=True, null=True)),
                ('online_resource', models.CharField(blank=True, max_length=1000, null=True)),
                ('capabilities_original_uri', models.CharField(blank=True, max_length=1000, null=True)),
                ('service_metadata_original_uri', models.CharField(blank=True, max_length=1000, null=True)),
                ('access_constraints', models.TextField(blank=True, null=True)),
                ('fees', models.TextField(blank=True, null=True)),
                ('last_remote_change', models.DateTimeField(blank=True, null=True)),
                ('status', models.IntegerField(blank=True, null=True)),
                ('spatial_res_type', models.CharField(blank=True, max_length=100, null=True)),
                ('spatial_res_value', models.CharField(blank=True, max_length=100, null=True)),
                ('is_broken', models.BooleanField(default=False)),
                ('is_custom', models.BooleanField(default=False)),
                ('is_inspire_conform', models.BooleanField(default=False)),
                ('has_inspire_downloads', models.BooleanField(default=False)),
                ('bounding_geometry', django.contrib.gis.db.models.fields.PolygonField(default=django.contrib.gis.geos.polygon.Polygon(((0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0))), srid=4326)),
                ('use_proxy_uri', models.BooleanField(default=False)),
                ('log_proxy_access', models.BooleanField(default=False)),
                ('is_secured', models.BooleanField(default=False)),
                ('authority_url', models.CharField(blank=True, max_length=255, null=True)),
                ('metadata_url', models.CharField(blank=True, max_length=255, null=True)),
                ('metadata_type', models.CharField(blank=True, choices=[(None, '---'), ('dataset', 'dataset'), ('service', 'service'), ('layer', 'layer'), ('tile', 'tile'), ('series', 'series'), ('featureType', 'featureType'), ('catalogue', 'catalogue'), ('attribute', 'attribute'), ('attributeType', 'attributeType'), ('collectionHardware', 'collectionHardware'), ('collectionSession', 'collectionSession'), ('nonGeographicDataset', 'nonGeographicDataset'), ('dimensionGroup', 'dimensionGroup'), ('feature', 'feature'), ('propertyType', 'propertyType'), ('fieldSession', 'fieldSession'), ('software', 'software'), ('model', 'model')], max_length=500, null=True, validators=[MrMap.validators.validate_metadata_enum_choices])),
                ('hits', models.IntegerField(default=0)),
                ('language_code', models.CharField(blank=True, choices=[('ger', 'German'), ('eng', 'English')], default='ger', max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MetadataRelation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('relation_type', models.CharField(blank=True, choices=[(None, '---'), ('visualizes', 'visualizes'), ('describes', 'describes'), ('harvestedThrough', 'harvestedThrough'), ('harvestedParent', 'harvestedParent')], max_length=255, null=True)),
                ('internal', models.BooleanField(default=False)),
                ('origin', models.CharField(blank=True, choices=[(None, '---'), ('Capabilities', 'Capabilities'), ('Upload', 'Upload'), ('Editor', 'Editor'), ('Catalogue', 'Catalogue')], max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MimeType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('public_id', models.CharField(blank=True, max_length=255, null=True, unique=True, validators=[MrMap.validators.not_uuid])),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('last_modified', models.DateTimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('operation', models.CharField(choices=[(None, '---'), ('GetCapabilities', 'GetCapabilities'), ('GetMap', 'GetMap'), ('GetFeatureInfo', 'GetFeatureInfo'), ('DescribeLayer', 'DescribeLayer'), ('GetLegendGraphic', 'GetLegendGraphic'), ('GetStyles', 'GetStyles'), ('PutStyles', 'PutStyles'), ('GetFeature', 'GetFeature'), ('Transaction', 'Transaction'), ('LockFeature', 'LockFeature'), ('DescribeFeatureType', 'DescribeFeatureType'), ('GetFeatureWithLock', 'GetFeatureWithLock'), ('GetGmlObject', 'GetGmlObject'), ('ListStoredQueries', 'ListStoredQueries'), ('GetPropertyValue', 'GetPropertyValue'), ('DescribeStoredQueries', 'DescribeStoredQueries'), ('GetRecords', 'GetRecords'), ('DescribeRecord', 'DescribeRecord'), ('GetRecordById', 'GetRecordById')], max_length=255, null=True)),
                ('mime_type', models.CharField(max_length=500)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Namespace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('version', models.CharField(blank=True, max_length=50, null=True)),
                ('uri', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='OGCOperation',
            fields=[
                ('operation', models.CharField(choices=[(None, '---'), ('GetCapabilities', 'GetCapabilities'), ('GetMap', 'GetMap'), ('GetFeatureInfo', 'GetFeatureInfo'), ('DescribeLayer', 'DescribeLayer'), ('GetLegendGraphic', 'GetLegendGraphic'), ('GetStyles', 'GetStyles'), ('PutStyles', 'PutStyles'), ('GetFeature', 'GetFeature'), ('Transaction', 'Transaction'), ('LockFeature', 'LockFeature'), ('DescribeFeatureType', 'DescribeFeatureType'), ('GetFeatureWithLock', 'GetFeatureWithLock'), ('GetGmlObject', 'GetGmlObject'), ('ListStoredQueries', 'ListStoredQueries'), ('GetPropertyValue', 'GetPropertyValue'), ('DescribeStoredQueries', 'DescribeStoredQueries'), ('GetRecords', 'GetRecords'), ('DescribeRecord', 'DescribeRecord'), ('GetRecordById', 'GetRecordById')], max_length=255, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='ProxyLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation', models.CharField(blank=True, max_length=100, null=True)),
                ('uri', models.CharField(blank=True, max_length=1000, null=True)),
                ('post_body', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('response_wfs_num_features', models.IntegerField(blank=True, null=True)),
                ('response_wms_megapixel', models.FloatField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='ReferenceSystem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('prefix', models.CharField(default='EPSG:', max_length=255)),
                ('version', models.CharField(default='9.6.1', max_length=50)),
            ],
            options={
                'ordering': ['-code'],
            },
        ),
        migrations.CreateModel(
            name='RequestOperation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation_name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('public_id', models.CharField(blank=True, max_length=255, null=True, unique=True, validators=[MrMap.validators.not_uuid])),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('last_modified', models.DateTimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_root', models.BooleanField(default=False)),
                ('availability', models.DecimalField(decimal_places=2, default=0.0, max_digits=4)),
                ('is_available', models.BooleanField(default=False)),
                ('keep_custom_md', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[(None, '---'), ('wms', 'wms'), ('wfs', 'wfs'), ('wmc', 'wmc'), ('dataset', 'dataset'), ('csw', 'csw')], max_length=100)),
                ('version', models.CharField(choices=[(None, '---'), ('1.0.0', '1.0.0'), ('1.1.0', '1.1.0'), ('1.1.1', '1.1.1'), ('1.3.0', '1.3.0'), ('2.0.0', '2.0.0'), ('2.0.2', '2.0.2')], max_length=100)),
                ('specification', models.URLField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('legend_uri', models.CharField(blank=True, max_length=500, null=True)),
                ('height', models.IntegerField(blank=True, null=True)),
                ('width', models.IntegerField(blank=True, null=True)),
                ('mime_type', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Layer',
            fields=[
                ('service_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='service.service')),
                ('identifier', models.CharField(max_length=500, null=True)),
                ('preview_image', models.CharField(blank=True, max_length=100, null=True)),
                ('preview_extent', models.CharField(blank=True, max_length=100, null=True)),
                ('preview_legend', models.CharField(max_length=100)),
                ('is_queryable', models.BooleanField(default=False)),
                ('is_opaque', models.BooleanField(default=False)),
                ('is_cascaded', models.BooleanField(default=False)),
                ('scale_min', models.FloatField(default=0)),
                ('scale_max', models.FloatField(default=0)),
                ('bbox_lat_lon', django.contrib.gis.db.models.fields.PolygonField(default=django.contrib.gis.geos.polygon.Polygon(((-90.0, -180.0), (-90.0, 180.0), (90.0, 180.0), (90.0, -180.0), (-90.0, -180.0))), srid=4326)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('service.service', models.Model),
            managers=[
                ('_tree_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('service_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='service.service')),
                ('type', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=('service.service',),
        ),
        migrations.CreateModel(
            name='ServiceUrl',
            fields=[
                ('genericurl_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='service.genericurl')),
                ('operation', models.CharField(blank=True, choices=[(None, '---'), ('GetCapabilities', 'GetCapabilities'), ('GetMap', 'GetMap'), ('GetFeatureInfo', 'GetFeatureInfo'), ('DescribeLayer', 'DescribeLayer'), ('GetLegendGraphic', 'GetLegendGraphic'), ('GetStyles', 'GetStyles'), ('PutStyles', 'PutStyles'), ('GetFeature', 'GetFeature'), ('Transaction', 'Transaction'), ('LockFeature', 'LockFeature'), ('DescribeFeatureType', 'DescribeFeatureType'), ('GetFeatureWithLock', 'GetFeatureWithLock'), ('GetGmlObject', 'GetGmlObject'), ('ListStoredQueries', 'ListStoredQueries'), ('GetPropertyValue', 'GetPropertyValue'), ('DescribeStoredQueries', 'DescribeStoredQueries'), ('GetRecords', 'GetRecords'), ('DescribeRecord', 'DescribeRecord'), ('GetRecordById', 'GetRecordById')], max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('service.genericurl',),
        ),
    ]
