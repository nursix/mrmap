# Generated by Django 3.1.7 on 2021-04-01 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0003_auto_20210401_1400'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='monitoringresult',
            unique_together=set(),
        ),
    ]
