# Generated by Django 3.1.8 on 2021-04-27 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acl', '0006_auto_20210427_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genericobjectrelation',
            name='search_helper',
            field=models.TextField(default='', editable=False),
        ),
    ]
