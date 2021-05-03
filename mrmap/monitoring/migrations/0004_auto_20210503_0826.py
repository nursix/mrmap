# Generated by Django 3.1.8 on 2021-05-03 06:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('monitoring', '0003_auto_20210430_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='healthstate',
            name='created_by_user',
            field=models.ForeignKey(blank=True, help_text='The user who has created this object.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='monitoring_healthstate_created_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AlterField(
            model_name='healthstate',
            name='last_modified_by',
            field=models.ForeignKey(blank=True, help_text='The last user who has modified this object.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='monitoring_healthstate_last_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='Last modified by'),
        ),
        migrations.AlterField(
            model_name='monitoringresult',
            name='created_by_user',
            field=models.ForeignKey(blank=True, help_text='The user who has created this object.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='monitoring_monitoringresult_created_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AlterField(
            model_name='monitoringresult',
            name='last_modified_by',
            field=models.ForeignKey(blank=True, help_text='The last user who has modified this object.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='monitoring_monitoringresult_last_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='Last modified by'),
        ),
        migrations.AlterField(
            model_name='monitoringrun',
            name='created_by_user',
            field=models.ForeignKey(blank=True, help_text='The user who has created this object.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='monitoring_monitoringrun_created_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AlterField(
            model_name='monitoringrun',
            name='last_modified_by',
            field=models.ForeignKey(blank=True, help_text='The last user who has modified this object.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='monitoring_monitoringrun_last_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='Last modified by'),
        ),
    ]
