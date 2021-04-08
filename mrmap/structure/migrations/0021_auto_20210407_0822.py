# Generated by Django 3.1.7 on 2021-04-07 06:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0020_auto_20210406_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupinvitationrequest',
            name='activation_until',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 7, 6, 22, 6, 494461, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='publishrequest',
            name='activation_until',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 7, 6, 22, 6, 494461, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='useractivation',
            name='activation_until',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 7, 6, 22, 6, 493427, tzinfo=utc)),
        ),
    ]
