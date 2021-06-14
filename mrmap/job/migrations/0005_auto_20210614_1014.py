# Generated by Django 3.1.8 on 2021-06-14 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0006_auto_20210614_1014'),
        ('job', '0004_auto_20210610_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='owned_by_org',
            field=models.ForeignKey(blank=True, editable=False, help_text='The organization which is the owner of this object.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='job_job_owned_by_org', to='structure.organization', verbose_name='Owner'),
        ),
        migrations.AlterField(
            model_name='task',
            name='owned_by_org',
            field=models.ForeignKey(blank=True, editable=False, help_text='The organization which is the owner of this object.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='job_task_owned_by_org', to='structure.organization', verbose_name='Owner'),
        ),
    ]
