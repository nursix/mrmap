# Generated by Django 3.1.7 on 2021-03-15 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_auto_20210315_1550'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='metadata',
            options={'permissions': [('delete_dataset_metadata', 'Can delete dataset metadata'), ('add_dataset_metadata', 'Can add dataset metadata'), ('activate_resource', 'Can activate a resource'), ('update_resource', 'Can update a resource'), ('harvest_resource', 'Can harvest a resource'), ('add_resource', 'Can add new resources'), ('delete_resource', 'Can delete resources')]},
        ),
    ]