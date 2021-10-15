# Generated by Django 3.2.7 on 2021-10-15 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0003_auto_20211015_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='mapcontextlayer',
            name='layer_scale_max',
            field=models.FloatField(blank=True, editable=False, help_text='maximum scale for a possible request to this layer. If the request is out of the given scope, the service will response with empty transparentimages. None value means no restriction.', null=True, verbose_name='scale maximum value'),
        ),
        migrations.AddField(
            model_name='mapcontextlayer',
            name='layer_scale_min',
            field=models.FloatField(blank=True, editable=False, help_text='minimum scale for a possible request to this layer. If the request is out of the given scope, the service will response with empty transparentimages. None value means no restriction.', null=True, verbose_name='scale minimum value'),
        ),
    ]
