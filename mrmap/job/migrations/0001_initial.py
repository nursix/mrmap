# Generated by Django 3.2.4 on 2021-07-09 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, help_text='The timestamp of the creation date of this object.', verbose_name='Created at')),
                ('last_modified_at', models.DateTimeField(auto_now=True, db_index=True, help_text='The timestamp of the last modification of this object', verbose_name='Last modified at')),
                ('name', models.CharField(help_text='Describe what this job does.', max_length=256, verbose_name='name')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, help_text='The timestamp of the creation date of this object.', verbose_name='Created at')),
                ('last_modified_at', models.DateTimeField(auto_now=True, db_index=True, help_text='The timestamp of the last modification of this object', verbose_name='Last modified at')),
                ('status', models.CharField(choices=[(None, '---'), ('pending', 'pending'), ('started', 'started'), ('success', 'success'), ('failure', 'failure')], default='pending', help_text='Current state of the task being run', max_length=50, verbose_name='task state')),
                ('name', models.CharField(help_text='Describe what this job does.', max_length=256, verbose_name='name')),
                ('phase', models.TextField(default='')),
                ('progress', models.FloatField(default=0.0)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('done_at', models.DateTimeField(blank=True, null=True)),
                ('traceback', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-done_at'],
            },
        ),
    ]
