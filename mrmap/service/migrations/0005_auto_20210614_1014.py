# Generated by Django 3.1.8 on 2021-06-14 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0006_auto_20210614_1014'),
        ('service', '0004_auto_20210608_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allowedoperation',
            name='owned_by_org',
            field=models.ForeignKey(blank=True, editable=False, help_text='The organization which is the owner of this object.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_allowedoperation_owned_by_org', to='structure.organization', verbose_name='Owner'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='owned_by_org',
            field=models.ForeignKey(blank=True, editable=False, help_text='The organization which is the owner of this object.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_dataset_owned_by_org', to='structure.organization', verbose_name='Owner'),
        ),
        migrations.AlterField(
            model_name='document',
            name='owned_by_org',
            field=models.ForeignKey(blank=True, editable=False, help_text='The organization which is the owner of this object.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_document_owned_by_org', to='structure.organization', verbose_name='Owner'),
        ),
        migrations.AlterField(
            model_name='externalauthentication',
            name='owned_by_org',
            field=models.ForeignKey(blank=True, editable=False, help_text='The organization which is the owner of this object.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_externalauthentication_owned_by_org', to='structure.organization', verbose_name='Owner'),
        ),
        migrations.AlterField(
            model_name='featuretype',
            name='owned_by_org',
            field=models.ForeignKey(blank=True, editable=False, help_text='The organization which is the owner of this object.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_featuretype_owned_by_org', to='structure.organization', verbose_name='Owner'),
        ),
        migrations.AlterField(
            model_name='featuretypeelement',
            name='owned_by_org',
            field=models.ForeignKey(blank=True, editable=False, help_text='The organization which is the owner of this object.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_featuretypeelement_owned_by_org', to='structure.organization', verbose_name='Owner'),
        ),
        migrations.AlterField(
            model_name='genericurl',
            name='owned_by_org',
            field=models.ForeignKey(blank=True, editable=False, help_text='The organization which is the owner of this object.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_genericurl_owned_by_org', to='structure.organization', verbose_name='Owner'),
        ),
        migrations.AlterField(
            model_name='metadata',
            name='owned_by_org',
            field=models.ForeignKey(blank=True, editable=False, help_text='The organization which is the owner of this object.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_metadata_owned_by_org', to='structure.organization', verbose_name='Owner'),
        ),
        migrations.AlterField(
            model_name='proxylog',
            name='owned_by_org',
            field=models.ForeignKey(blank=True, editable=False, help_text='The organization which is the owner of this object.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_proxylog_owned_by_org', to='structure.organization', verbose_name='Owner'),
        ),
        migrations.AlterField(
            model_name='service',
            name='owned_by_org',
            field=models.ForeignKey(blank=True, editable=False, help_text='The organization which is the owner of this object.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_service_owned_by_org', to='structure.organization', verbose_name='Owner'),
        ),
        migrations.AlterField(
            model_name='serviceurl',
            name='owned_by_org',
            field=models.ForeignKey(blank=True, editable=False, help_text='The organization which is the owner of this object.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_serviceurl_owned_by_org', to='structure.organization', verbose_name='Owner'),
        ),
    ]
