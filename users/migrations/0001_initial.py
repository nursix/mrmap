# Generated by Django 3.1.7 on 2021-03-11 09:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('service', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('notify_on_update', models.BooleanField(default=True, help_text='Sends an e-mai if the service has been updated.', verbose_name='Notify on update')),
                ('notify_on_metadata_edit', models.BooleanField(default=True, help_text="Sends an e-mai if the service's metadata has been changed.", verbose_name='Notify on metadata edit')),
                ('notify_on_access_edit', models.BooleanField(default=True, help_text="Sends an e-mai if the service's access has been changed.", verbose_name='Notify on access edit')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('metadata', models.ForeignKey(help_text='Select the service you want to subscribe. When you edit an existing subscription, you can not change this selection.', on_delete=django.db.models.deletion.CASCADE, to='service.metadata', verbose_name='Service')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('metadata', 'user')},
            },
        ),
    ]
