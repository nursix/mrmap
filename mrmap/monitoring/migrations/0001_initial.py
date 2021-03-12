# Generated by Django 3.1.7 on 2021-03-11 17:36

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HealthState',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='Health state')),
                ('health_state_code', models.CharField(choices=[('ok', 'ok'), ('warning', 'warning'), ('critical', 'critical'), ('unknown', 'unknown'), ('unauthorized', 'unauthorized')], default='unknown', max_length=12, verbose_name='Health state code')),
                ('health_message', models.CharField(default='The health state is unknown, cause no health checks runs for this resource.', max_length=512)),
                ('reliability_1w', models.FloatField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)])),
                ('reliability_1m', models.FloatField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)])),
                ('reliability_3m', models.FloatField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)])),
                ('average_response_time', models.DurationField(blank=True, null=True)),
                ('average_response_time_1w', models.DurationField(blank=True, null=True)),
                ('average_response_time_1m', models.DurationField(blank=True, null=True)),
                ('average_response_time_3m', models.DurationField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Health state',
                'verbose_name_plural': 'Health states',
                'ordering': ['-monitoring_run__start'],
            },
        ),
        migrations.CreateModel(
            name='HealthStateReason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField(verbose_name='Reason')),
                ('health_state_code', models.CharField(choices=[('ok', 'ok'), ('warning', 'warning'), ('critical', 'critical'), ('unknown', 'unknown'), ('unauthorized', 'unauthorized')], default='unknown', max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='MonitoringResult',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='Result')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('duration', models.DurationField(blank=True, null=True)),
                ('status_code', models.IntegerField(blank=True, null=True)),
                ('error_msg', models.TextField(blank=True, null=True)),
                ('available', models.BooleanField(null=True)),
                ('monitored_uri', models.CharField(max_length=2000)),
            ],
            options={
                'verbose_name': 'Monitoring result',
                'verbose_name_plural': 'Monitoring results',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='MonitoringRun',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='Monitoring run')),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('duration', models.DurationField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Monitoring run',
                'verbose_name_plural': 'Monitoring runs',
                'ordering': ['-end'],
            },
        ),
        migrations.CreateModel(
            name='MonitoringSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_time', models.TimeField()),
                ('timeout', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MonitoringResultCapability',
            fields=[
                ('monitoringresult_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='monitoring.monitoringresult')),
                ('needs_update', models.BooleanField(blank=True, null=True)),
                ('diff', models.TextField(blank=True, null=True)),
            ],
            bases=('monitoring.monitoringresult',),
        ),
    ]