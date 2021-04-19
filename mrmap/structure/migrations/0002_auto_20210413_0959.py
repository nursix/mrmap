# Generated by Django 3.1.8 on 2021-04-13 07:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupinvitationrequest',
            name='activation_until',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 13, 7, 59, 40, 314010, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='publishrequest',
            name='activation_until',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 13, 7, 59, 40, 314010, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='useractivation',
            name='activation_until',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 13, 7, 59, 40, 313446, tzinfo=utc)),
        ),
    ]
