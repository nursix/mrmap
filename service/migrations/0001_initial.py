# Generated by Django 3.1 on 2020-10-02 08:05

import MrMap.validators
from django.conf import settings
import django.contrib.gis.db.models.fields
import django.contrib.gis.geos.polygon
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('structure', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('public_id', models.CharField(blank=True, max_length=255, null=True, unique=True, validators=[MrMap.validators.not_uuid])),
                ('created', models.DateTimeField(auto_now_add=True)),
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
                ('created', models.DateTimeField(auto_now_add=True)),
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
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('document_type', models.CharField(choices=[(None, '---'), ('Capability', 'Capability'), ('Metadata', 'Metadata')], max_length=255, null=True, validators=[MrMap.validators.validate_document_enum_choices])),
                ('content', models.TextField(blank=True, null=True)),
                ('is_original', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
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
                ('created', models.DateTimeField(auto_now_add=True)),
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
                ('created', models.DateTimeField(auto_now_add=True)),
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
                ('created', models.DateTimeField(auto_now_add=True)),
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
                ('date', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='service.legaldate')),
            ],
        ),
        migrations.CreateModel(
            name='Licence',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('public_id', models.CharField(blank=True, max_length=255, null=True, unique=True, validators=[MrMap.validators.not_uuid])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('identifier', models.CharField(max_length=255, unique=True)),
                ('symbol_url', models.URLField(null=True)),
                ('description', models.TextField()),
                ('description_url', models.URLField(null=True)),
                ('is_open_data', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='structure.mrmapgroup')),
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
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('identifier', models.CharField(max_length=1000, null=True)),
                ('title', models.CharField(max_length=1000)),
                ('abstract', models.TextField(blank=True, null=True)),
                ('online_resource', models.CharField(blank=True, max_length=1000, null=True)),
                ('capabilities_original_uri', models.CharField(blank=True, max_length=1000, null=True)),
                ('service_metadata_original_uri', models.CharField(blank=True, max_length=1000, null=True)),
                ('access_constraints', models.TextField(blank=True, null=True)),
                ('fees', models.TextField(blank=True, null=True)),
                ('last_remote_change', models.DateTimeField(blank=True, null=True)),
                ('status', models.IntegerField(blank=True, null=True)),
                ('use_proxy_uri', models.BooleanField(default=False)),
                ('log_proxy_access', models.BooleanField(default=False)),
                ('spatial_res_type', models.CharField(blank=True, max_length=100, null=True)),
                ('spatial_res_value', models.CharField(blank=True, max_length=100, null=True)),
                ('is_broken', models.BooleanField(default=False)),
                ('is_custom', models.BooleanField(default=False)),
                ('is_inspire_conform', models.BooleanField(default=False)),
                ('has_inspire_downloads', models.BooleanField(default=False)),
                ('bounding_geometry', django.contrib.gis.db.models.fields.PolygonField(default=django.contrib.gis.geos.polygon.Polygon(((0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0))), srid=4326)),
                ('is_secured', models.BooleanField(default=False)),
                ('authority_url', models.CharField(blank=True, max_length=255, null=True)),
                ('metadata_url', models.CharField(blank=True, max_length=255, null=True)),
                ('metadata_type', models.CharField(blank=True, choices=[(None, '---'), ('dataset', 'dataset'), ('service', 'service'), ('layer', 'layer'), ('tile', 'tile'), ('series', 'series'), ('featureType', 'featureType'), ('catalogue', 'catalogue'), ('attribute', 'attribute'), ('attributeType', 'attributeType'), ('collectionHardware', 'collectionHardware'), ('collectionSession', 'collectionSession'), ('nonGeographicDataset', 'nonGeographicDataset'), ('dimensionGroup', 'dimensionGroup'), ('feature', 'feature'), ('propertyType', 'propertyType'), ('fieldSession', 'fieldSession'), ('software', 'software'), ('model', 'model')], max_length=500, null=True, validators=[MrMap.validators.validate_metadata_enum_choices])),
                ('hits', models.IntegerField(default=0)),
                ('language_code', models.CharField(choices=[('ger', 'German'), ('eng', 'English')], default='ger', max_length=100)),
                ('additional_urls', models.ManyToManyField(blank=True, to='service.GenericUrl')),
                ('categories', models.ManyToManyField(blank=True, to='service.Category')),
                ('contact', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='structure.organization')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='structure.mrmapgroup')),
                ('dimensions', models.ManyToManyField(blank=True, to='service.Dimension')),
            ],
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
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_root', models.BooleanField(default=False)),
                ('availability', models.DecimalField(decimal_places=2, default=0.0, max_digits=4)),
                ('is_available', models.BooleanField(default=False)),
                ('keep_custom_md', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='structure.mrmapgroup')),
                ('created_by_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('is_update_candidate_for', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_update_candidate', to='service.service')),
                ('metadata', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='service', to='service.metadata')),
                ('parent_service', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_service', to='service.service')),
                ('published_for', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='published_for', to='structure.organization')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
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
                ('position', models.IntegerField(default=0)),
                ('is_queryable', models.BooleanField(default=False)),
                ('is_opaque', models.BooleanField(default=False)),
                ('is_cascaded', models.BooleanField(default=False)),
                ('scale_min', models.FloatField(default=0)),
                ('scale_max', models.FloatField(default=0)),
                ('bbox_lat_lon', django.contrib.gis.db.models.fields.PolygonField(default=django.contrib.gis.geos.polygon.Polygon(((-90.0, -180.0), (-90.0, 180.0), (90.0, 180.0), (90.0, -180.0), (-90.0, -180.0))), srid=4326)),
            ],
            options={
                'ordering': ['position'],
            },
            bases=('service.service',),
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
        migrations.AddField(
            model_name='service',
            name='service_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='service.servicetype'),
        ),
        migrations.CreateModel(
            name='SecuredOperation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('operation', models.CharField(blank=True, choices=[(None, '---'), ('GetCapabilities', 'GetCapabilities'), ('GetMap', 'GetMap'), ('GetFeatureInfo', 'GetFeatureInfo'), ('DescribeLayer', 'DescribeLayer'), ('GetLegendGraphic', 'GetLegendGraphic'), ('GetStyles', 'GetStyles'), ('PutStyles', 'PutStyles'), ('GetFeature', 'GetFeature'), ('Transaction', 'Transaction'), ('LockFeature', 'LockFeature'), ('DescribeFeatureType', 'DescribeFeatureType'), ('GetFeatureWithLock', 'GetFeatureWithLock'), ('GetGmlObject', 'GetGmlObject'), ('ListStoredQueries', 'ListStoredQueries'), ('GetPropertyValue', 'GetPropertyValue'), ('DescribeStoredQueries', 'DescribeStoredQueries'), ('GetRecords', 'GetRecords'), ('DescribeRecord', 'DescribeRecord'), ('GetRecordById', 'GetRecordById')], max_length=255, null=True)),
                ('bounding_geometry', django.contrib.gis.db.models.fields.GeometryCollectionField(blank=True, null=True, srid=4326)),
                ('allowed_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='allowed_operations', to='structure.mrmapgroup')),
                ('secured_metadata', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='secured_operations', to='service.metadata')),
            ],
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
                'unique_together': {('code', 'prefix')},
            },
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
                ('metadata', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='service.metadata')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='MimeType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('public_id', models.CharField(blank=True, max_length=255, null=True, unique=True, validators=[MrMap.validators.not_uuid])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('operation', models.CharField(choices=[(None, '---'), ('GetCapabilities', 'GetCapabilities'), ('GetMap', 'GetMap'), ('GetFeatureInfo', 'GetFeatureInfo'), ('DescribeLayer', 'DescribeLayer'), ('GetLegendGraphic', 'GetLegendGraphic'), ('GetStyles', 'GetStyles'), ('PutStyles', 'PutStyles'), ('GetFeature', 'GetFeature'), ('Transaction', 'Transaction'), ('LockFeature', 'LockFeature'), ('DescribeFeatureType', 'DescribeFeatureType'), ('GetFeatureWithLock', 'GetFeatureWithLock'), ('GetGmlObject', 'GetGmlObject'), ('ListStoredQueries', 'ListStoredQueries'), ('GetPropertyValue', 'GetPropertyValue'), ('DescribeStoredQueries', 'DescribeStoredQueries'), ('GetRecords', 'GetRecords'), ('DescribeRecord', 'DescribeRecord'), ('GetRecordById', 'GetRecordById')], max_length=255, null=True)),
                ('mime_type', models.CharField(max_length=500)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='structure.mrmapgroup')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MetadataRelation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('relation_type', models.CharField(blank=True, choices=[(None, '---'), ('visualizes', 'visualizes'), ('describedBy', 'describedBy'), ('harvestedThrough', 'harvestedThrough'), ('harvestedParent', 'harvestedParent')], max_length=255, null=True)),
                ('internal', models.BooleanField(default=False)),
                ('origin', models.CharField(blank=True, choices=[(None, '---'), ('Capabilities', 'Capabilities'), ('Upload', 'Upload'), ('Editor', 'Editor'), ('Catalogue', 'Catalogue')], max_length=255, null=True)),
                ('metadata_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.metadata')),
            ],
        ),
        migrations.AddField(
            model_name='metadata',
            name='formats',
            field=models.ManyToManyField(blank=True, to='service.MimeType'),
        ),
        migrations.AddField(
            model_name='metadata',
            name='keywords',
            field=models.ManyToManyField(to='service.Keyword'),
        ),
        migrations.AddField(
            model_name='metadata',
            name='legal_dates',
            field=models.ManyToManyField(blank=True, to='service.LegalDate'),
        ),
        migrations.AddField(
            model_name='metadata',
            name='legal_reports',
            field=models.ManyToManyField(blank=True, to='service.LegalReport'),
        ),
        migrations.AddField(
            model_name='metadata',
            name='licence',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='service.licence'),
        ),
        migrations.AddField(
            model_name='metadata',
            name='reference_system',
            field=models.ManyToManyField(blank=True, to='service.ReferenceSystem'),
        ),
        migrations.AddField(
            model_name='metadata',
            name='related_metadata',
            field=models.ManyToManyField(blank=True, to='service.MetadataRelation'),
        ),
        migrations.AddIndex(
            model_name='keyword',
            index=models.Index(fields=['keyword'], name='service_key_keyword_a43a85_idx'),
        ),
        migrations.AddField(
            model_name='genericurl',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='structure.mrmapgroup'),
        ),
        migrations.AddField(
            model_name='featuretypeelement',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='structure.mrmapgroup'),
        ),
        migrations.AddField(
            model_name='featuretype',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='structure.mrmapgroup'),
        ),
        migrations.AddField(
            model_name='featuretype',
            name='default_srs',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='default_srs', to='service.referencesystem'),
        ),
        migrations.AddField(
            model_name='featuretype',
            name='elements',
            field=models.ManyToManyField(to='service.FeatureTypeElement'),
        ),
        migrations.AddField(
            model_name='featuretype',
            name='metadata',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='featuretype', to='service.metadata'),
        ),
        migrations.AddField(
            model_name='featuretype',
            name='namespaces',
            field=models.ManyToManyField(to='service.Namespace'),
        ),
        migrations.AddField(
            model_name='featuretype',
            name='parent_service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='featuretypes', to='service.service'),
        ),
        migrations.AddField(
            model_name='externalauthentication',
            name='metadata',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='external_authentication', to='service.metadata'),
        ),
        migrations.AddField(
            model_name='document',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='structure.mrmapgroup'),
        ),
        migrations.AddField(
            model_name='document',
            name='metadata',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='service.metadata'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='structure.mrmapgroup'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='metadata',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dataset', to='service.metadata'),
        ),
        migrations.AddField(
            model_name='category',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='structure.mrmapgroup'),
        ),
        migrations.AddField(
            model_name='style',
            name='layer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='style', to='service.layer'),
        ),
        migrations.AddField(
            model_name='service',
            name='operation_urls',
            field=models.ManyToManyField(to='service.ServiceUrl'),
        ),
        migrations.AddIndex(
            model_name='metadata',
            index=models.Index(fields=['id', 'public_id', 'identifier'], name='service_met_id_fa3740_idx'),
        ),
        migrations.AddField(
            model_name='layer',
            name='parent_layer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_layers', to='service.layer'),
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['title_EN'], name='service_cat_title_E_d0a3ab_idx'),
        ),
    ]
