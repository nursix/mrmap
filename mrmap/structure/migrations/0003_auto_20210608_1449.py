# Generated by Django 3.2.3 on 2021-06-08 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0002_auto_20210607_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationpublishrelation',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='pendingtask',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
