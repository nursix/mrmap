# Generated by Django 3.1.7 on 2021-04-14 11:08

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0003_auto_20210413_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupinvitationrequest',
            name='activation_until',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 14, 11, 8, 39, 910833, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='publishrequest',
            name='activation_until',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 14, 11, 8, 39, 910833, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='useractivation',
            name='activation_until',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 14, 11, 8, 39, 909667, tzinfo=utc)),
        ),
    ]