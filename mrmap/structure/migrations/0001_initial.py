<<<<<<< HEAD
# Generated by Django 3.1.7 on 2021-03-25 14:09
=======
# Generated by Django 3.1.8 on 2021-04-13 07:35
>>>>>>> 6547e7f6ad710c8351a3ede267a054c17a44fa14

import datetime
<<<<<<< HEAD
import django.core.validators
from django.db import migrations, models
=======
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.tokens
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions
>>>>>>> 6547e7f6ad710c8351a3ede267a054c17a44fa14
from django.utils.timezone import utc
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
<<<<<<< HEAD
            name='ErrorReport',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('message', models.TextField()),
                ('traceback', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
=======
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
                ('confirmed_newsletter', models.BooleanField(default=False, verbose_name='I want to sign up for the newsletter')),
                ('confirmed_survey', models.BooleanField(default=False, verbose_name='I want to participate in surveys')),
                ('confirmed_dsgvo', models.DateTimeField(auto_now_add=True, verbose_name='I understand and accept that my data will be automatically processed and securely stored, as it is stated in the general data protection regulation (GDPR).')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
>>>>>>> 6547e7f6ad710c8351a3ede267a054c17a44fa14
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('last_modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Last modified at')),
                ('person_name', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Contact person')),
                ('email', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='E-Mail')),
                ('phone', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Phone')),
                ('facsimile', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Facsimile')),
                ('city', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='City')),
                ('postal_code', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Postal code')),
                ('address_type', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Address type')),
                ('address', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Address')),
                ('state_or_province', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='State or province')),
                ('country', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Country')),
                ('organization_name', models.CharField(default='', help_text='The name of the organization', max_length=255, null=True, verbose_name='Organization name')),
                ('description', models.TextField(blank=True, default='', help_text='Describe what this organization representing', null=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'Organization',
                'verbose_name_plural': 'Organizations',
                'ordering': ['organization_name'],
                'permissions': [('remove_publisher', 'Can remove publisher')],
            },
        ),
        migrations.CreateModel(
<<<<<<< HEAD
            name='PendingTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('last_modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Last modified at')),
                ('task_id', models.CharField(blank=True, max_length=500, null=True)),
                ('description', models.TextField()),
                ('progress', models.FloatField(blank=True, default=0.0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('remaining_time', models.DurationField(blank=True, null=True)),
                ('is_finished', models.BooleanField(default=False)),
                ('type', models.CharField(blank=True, choices=[(None, '---'), ('harvest', 'harvest'), ('register', 'register'), ('validate', 'validate')], max_length=500, null=True, validators=[MrMap.validators.validate_pending_task_enum_choices])),
=======
            name='UserActivation',
            fields=[
                ('activation_until', models.DateTimeField(default=datetime.datetime(2021, 5, 13, 7, 35, 25, 446345, tzinfo=utc))),
                ('activation_hash', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=(models.Model, django.contrib.auth.tokens.PasswordResetTokenGenerator),
        ),
        migrations.CreateModel(
            name='MrMapGroup',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.group')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('is_public_group', models.BooleanField(default=False)),
                ('is_permission_group', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organization_groups', to='structure.organization')),
                ('parent_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='children_groups', to='structure.mrmapgroup')),
                ('publish_for_organizations', models.ManyToManyField(blank=True, related_name='publishers', to='structure.Organization')),
            ],
            options={
                'verbose_name': 'Group',
                'verbose_name_plural': 'Groups',
                'ordering': [django.db.models.expressions.Case(django.db.models.expressions.When(name='Public', then=0)), 'name'],
                'permissions': [('add_user_to_group', 'Can add user to a group'), ('remove_user_from_group', 'Can remove user from a group'), ('request_to_become_publisher', 'Can request to become publisher')],
            },
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='GroupInvitationRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('message', models.TextField(blank=True, null=True)),
                ('activation_until', models.DateTimeField(default=datetime.datetime(2021, 5, 13, 7, 35, 25, 447075, tzinfo=utc))),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('is_accepted', models.BooleanField(default=False, verbose_name='accepted')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.group')),
                ('group', models.ForeignKey(help_text='Invite the selected user to this group.', on_delete=django.db.models.deletion.CASCADE, related_name='pending_group_invitations', to='structure.mrmapgroup', verbose_name='to group')),
                ('user', models.ForeignKey(help_text='Invite this user to a selected group.', on_delete=django.db.models.deletion.CASCADE, related_name='pending_group_invitations', to=settings.AUTH_USER_MODEL, verbose_name='Invited user')),
>>>>>>> 6547e7f6ad710c8351a3ede267a054c17a44fa14
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
<<<<<<< HEAD
=======
            name='GroupActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('metadata', models.CharField(blank=True, max_length=255, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='mrmapuser',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='primary_users', to='structure.organization'),
        ),
        migrations.AddField(
            model_name='mrmapuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.CreateModel(
>>>>>>> 6547e7f6ad710c8351a3ede267a054c17a44fa14
            name='PublishRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('last_modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Last modified at')),
                ('message', models.TextField(blank=True, null=True)),
<<<<<<< HEAD
                ('activation_until', models.DateTimeField(default=datetime.datetime(2021, 4, 24, 14, 9, 41, 528185, tzinfo=utc))),
                ('is_accepted', models.BooleanField(default=False, verbose_name='accepted')),
=======
                ('activation_until', models.DateTimeField(default=datetime.datetime(2021, 5, 13, 7, 35, 25, 447075, tzinfo=utc))),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('is_accepted', models.BooleanField(default=False, verbose_name='accepted')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.group')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pending_publish_requests', to='structure.mrmapgroup', verbose_name='group')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pending_publish_requests', to='structure.organization', verbose_name='organization')),
>>>>>>> 6547e7f6ad710c8351a3ede267a054c17a44fa14
            ],
            options={
                'verbose_name': 'Pending publish request',
                'verbose_name_plural': 'Pending publish requests',
<<<<<<< HEAD
=======
                'permissions': [('toggle_publish_requests', 'Can toggle publish requests')],
                'unique_together': {('group', 'organization')},
>>>>>>> 6547e7f6ad710c8351a3ede267a054c17a44fa14
            },
        ),
    ]
