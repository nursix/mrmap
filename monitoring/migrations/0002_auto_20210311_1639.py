# Generated by Django 3.1 on 2021-03-11 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_celery_beat', '0012_periodictask_expire_seconds'),
        ('monitoring', '0001_initial'),
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitoringsetting',
            name='metadatas',
            field=models.ManyToManyField(related_name='monitoring_setting', to='service.Metadata'),
        ),
        migrations.AddField(
            model_name='monitoringsetting',
            name='periodic_task',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='django_celery_beat.periodictask'),
        ),
        migrations.AddField(
            model_name='monitoring',
            name='metadata',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.metadata'),
        ),
        migrations.AddField(
            model_name='monitoring',
            name='monitoring_run',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monitoring_results', to='monitoring.monitoringrun'),
        ),
        migrations.AddField(
            model_name='healthstatereason',
            name='health_state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reasons', to='monitoring.healthstate'),
        ),
        migrations.AddField(
            model_name='healthstatereason',
            name='monitoring_result',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='health_state_reasons', to='monitoring.monitoring'),
        ),
        migrations.AddField(
            model_name='healthstate',
            name='metadata',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='health_state', to='service.metadata'),
        ),
        migrations.AddField(
            model_name='healthstate',
            name='monitoring_run',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoring.monitoringrun'),
        ),
    ]