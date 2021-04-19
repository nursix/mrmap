# Generated by Django 3.1.8 on 2021-04-15 11:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_auto_20210414_1308'),
        ('csw', '0002_harvestresult_service'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='harvestresult',
            name='service',
        ),
        migrations.AddField(
            model_name='harvestresult',
            name='metadata',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.metadata'),
            preserve_default=False,
        ),
    ]
