from django.db import models


class Permission(models.Model):
    can_create_organization = models.BooleanField(default=False)
    can_edit_organization = models.BooleanField(default=False)
    can_delete_organization = models.BooleanField(default=False)

    can_create_group = models.BooleanField(default=False)
    can_delete_group = models.BooleanField(default=False)
    can_edit_group = models.BooleanField(default=False)

    can_add_user_to_group = models.BooleanField(default=False)
    can_remove_user_from_group = models.BooleanField(default=False)

    can_change_group_role = models.BooleanField(default=False)

    can_activate_service = models.BooleanField(default=False)
    can_update_service = models.BooleanField(default=False)
    can_register_service = models.BooleanField(default=False)
    can_remove_service = models.BooleanField(default=False)

    can_react_to_publishing_requests = models.BooleanField(default=False)
    # more permissions coming

    def __str__(self):
        return str(self.id)

    def get_permission_list(self):
        p_list = []
        perms = self.__dict__
        del perms["id"]
        del perms["_state"]
        for perm_key, perm_val in perms.items():
            if perm_val:
                p_list.append(perm_key)
        return p_list


class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    person_name = models.CharField(max_length=200, default="", null=True)
    email = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    facsimile = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    postal_code = models.CharField(max_length=100, null=True)
    address_type = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    state_or_province = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.person_name

    class Meta:
        abstract = True


class Organization(Contact):
    organization_name = models.CharField(max_length=255, null=True, default="")
    description = models.TextField(null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    is_auto_generated = models.BooleanField(default=True)

    def __str__(self):
        if self.organization_name is None:
            return ""
        return self.organization_name


class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name="children")
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="groups")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)
    publish_for_organizations = models.ManyToManyField('Organization', related_name='can_publish_for', blank=True)
    created_by = models.ForeignKey('User', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class User(Contact):
    username = models.CharField(max_length=50)
    logged_in = models.BooleanField(default=False)
    salt = models.CharField(max_length=500)
    password = models.CharField(max_length=500)
    last_login = models.DateTimeField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField('Group', related_name='users')
    organization = models.ForeignKey('Organization', related_name='primary_users', on_delete=models.DO_NOTHING, null=True, blank=True)
    confirmed_newsletter = models.BooleanField(default=False)
    confirmed_survey = models.BooleanField(default=False)
    confirmed_dsgvo = models.DateTimeField(null=True, blank=True) # ToDo: For production this is not supposed to be nullable!!!
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class UserActivation(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.DO_NOTHING)
    activation_until = models.DateTimeField(null=True)
    activation_hash = models.CharField(max_length=500, null=False, blank=False)

    def __str__(self):
        return self.user.username


class PublishRequest(models.Model):
    group = models.ForeignKey(Group, related_name="pending_publish_requests", on_delete=models.DO_NOTHING)
    organization = models.ForeignKey(Organization, related_name="pending_publish_requests", on_delete=models.DO_NOTHING)
    message = models.TextField(null=True, blank=True)
    activation_until = models.DateTimeField(null=True)

    def __str__(self):
        return self.group.name + " > " + self.organization.organization_name
