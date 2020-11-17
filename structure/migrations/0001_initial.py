# Generated by Django 3.1.2 on 2020-11-16 12:48

import MrMap.validators
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MrMapUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('salt', models.CharField(max_length=500)),
                ('confirmed_newsletter', models.BooleanField(default=False)),
                ('confirmed_survey', models.BooleanField(default=False)),
                ('confirmed_dsgvo', models.DateTimeField(auto_now_add=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ErrorReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('traceback', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MrMapGroup',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.group')),
                ('description', models.TextField(blank=True)),
                ('is_public_group', models.BooleanField(default=False)),
                ('is_permission_group', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_name', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('email', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('phone', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('facsimile', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('city', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('postal_code', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('address_type', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('address', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('state_or_province', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('country', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('organization_name', models.CharField(default='', max_length=255, null=True)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('is_auto_generated', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_by', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='structure.organization')),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[(None, '---'), ('can_create_organization', 'can_create_organization'), ('can_edit_organization', 'can_edit_organization'), ('can_delete_organization', 'can_delete_organization'), ('can_create_group', 'can_create_group'), ('can_delete_group', 'can_delete_group'), ('can_edit_group', 'can_edit_group'), ('can_add_user_to_group', 'can_add_user_to_group'), ('can_remove_user_from_group', 'can_remove_user_from_group'), ('can_edit_group_role', 'can_edit_group_role'), ('can_edit_metadata', 'can_edit_metadata'), ('can_activate_resource', 'can_activate_resource'), ('can_update_resource', 'can_update_resource'), ('can_register_resource', 'can_register_resource'), ('can_remove_resource', 'can_remove_resource'), ('can_add_dataset_metadata', 'can_add_dataset_metadata'), ('can_remove_dataset_metadata', 'can_remove_dataset_metadata'), ('can_toggle_publish_requests', 'can_toggle_publish_requests'), ('can_remove_publisher', 'can_remove_publisher'), ('can_request_to_become_publisher', 'can_request_to_become_publisher'), ('can_generate_api_token', 'can_generate_api_token'), ('can_harvest', 'can_harvest'), ('can_access_logs', 'can_access_logs'), ('can_download_logs', 'can_download_logs'), ('can_run_monitoring', 'can_run_monitoring')], max_length=500, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserActivation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activation_until', models.DateTimeField(null=True)),
                ('activation_hash', models.CharField(max_length=500)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('permissions', models.ManyToManyField(to='structure.Permission')),
            ],
        ),
        migrations.CreateModel(
            name='PublishRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('message', models.TextField(blank=True, null=True)),
                ('activation_until', models.DateTimeField(null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publish_requests', to='structure.mrmapgroup')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publish_requests', to='structure.organization')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PendingTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(blank=True, max_length=500, null=True)),
                ('description', models.TextField()),
                ('progress', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('remaining_time', models.DurationField(blank=True, null=True)),
                ('is_finished', models.BooleanField(default=False)),
                ('type', models.CharField(blank=True, choices=[(None, '---'), ('harvest', 'harvest'), ('register', 'register')], max_length=500, null=True, validators=[MrMap.validators.validate_pending_task_enum_choices])),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='structure.mrmapgroup')),
                ('error_report', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='structure.errorreport')),
            ],
        ),
        migrations.AddField(
            model_name='mrmapgroup',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organization_groups', to='structure.organization'),
        ),
        migrations.AddField(
            model_name='mrmapgroup',
            name='parent_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='children_groups', to='structure.mrmapgroup'),
        ),
        migrations.AddField(
            model_name='mrmapgroup',
            name='publish_for_organizations',
            field=models.ManyToManyField(blank=True, related_name='can_publish_for', to='structure.Organization'),
        ),
        migrations.AddField(
            model_name='mrmapgroup',
            name='role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='structure.role'),
        ),
        migrations.CreateModel(
            name='GroupInvitationRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('message', models.TextField(blank=True, null=True)),
                ('activation_until', models.DateTimeField(null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('invited_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_invitations', to=settings.AUTH_USER_MODEL)),
                ('to_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='structure.mrmapgroup')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GroupActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('metadata', models.CharField(blank=True, max_length=255, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='structure.mrmapgroup')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='errorreport',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='structure.mrmapgroup'),
        ),
        migrations.AddField(
            model_name='mrmapuser',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='primary_users', to='structure.organization'),
        ),
        migrations.AddField(
            model_name='mrmapuser',
            name='theme',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_theme', to='structure.theme'),
        ),
        migrations.AddField(
            model_name='mrmapuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddConstraint(
            model_name='organization',
            constraint=models.UniqueConstraint(fields=('organization_name', 'person_name', 'email', 'phone', 'facsimile', 'city', 'postal_code', 'address_type', 'address', 'state_or_province', 'country', 'description'), name='unique organizations'),
        ),
    ]
