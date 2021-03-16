# Generated by Django 3.1.7 on 2021-03-16 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('service', '0006_auto_20210315_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.group'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.group'),
        ),
        migrations.AlterField(
            model_name='document',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.group'),
        ),
        migrations.AlterField(
            model_name='featuretype',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.group'),
        ),
        migrations.AlterField(
            model_name='featuretypeelement',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.group'),
        ),
        migrations.AlterField(
            model_name='genericurl',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.group'),
        ),
        migrations.AlterField(
            model_name='licence',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.group'),
        ),
        migrations.AlterField(
            model_name='metadata',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.group'),
        ),
        migrations.AlterField(
            model_name='mimetype',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.group'),
        ),
        migrations.AlterField(
            model_name='service',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.group'),
        ),
    ]