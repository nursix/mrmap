# Generated by Django 3.1.7 on 2021-04-01 10:35

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0013_auto_20210401_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupinvitationrequest',
            name='activation_until',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 1, 10, 34, 55, 696812, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='publishrequest',
            name='activation_until',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 1, 10, 34, 55, 696812, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='useractivation',
            name='activation_until',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 1, 10, 34, 55, 695774, tzinfo=utc)),
        ),
    ]