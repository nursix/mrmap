from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy
from django.views.generic import DetailView, DeleteView, UpdateView, CreateView
from guardian.mixins import LoginRequiredMixin, PermissionRequiredMixin, PermissionListMixin
from MrMap.views import CustomSingleTableMixin, SuccessMessageDeleteMixin, GenericViewContextMixin, InitFormMixin, \
    ConfirmView, DependingListView
from django.contrib.auth.mixins import PermissionRequiredMixin as DjangoPermissionRequiredMixin


class GenericPermissionMixin:
    action = None
    app_label = None
    model_name = None

    def get_model_data(self, model):
        self.app_label = model._meta.app_label
        self.model_name = model._meta.model_name.lower()

    def get_default_permission(self):
        """return the default view permission of the given model in format: 'app_label.model_name'"""
        if not self.action:
            raise ImproperlyConfigured("`GenericPermissionRequiredMixin` requires 'action' attribute to be set to "
                                       "default permission action like 'view' but is set to 'None'")
        self.get_model_data(self.model)
        return f"{self.app_label}.{self.action}_{self.model_name}"


class GenericPermissionRequiredMixin(GenericPermissionMixin, PermissionRequiredMixin):
    raise_exception = True
    action = None

    def get_required_permissions(self, request=None):
        """return the default view permission of the given model in format: 'app_label.model_name' if
        self.permission_required is None. Else the permission is generated by the self.action attribute.
        """
        if self.permission_required:
            return super().get_required_permissions(request=request)
        return [self.get_default_permission()]


class GenericPermissionListMixin(GenericPermissionMixin, PermissionListMixin):
    raise_exception = True
    action = None

    def get_required_permissions(self, request=None):
        """return the default view permission of the given model in format: 'app_label.model_name' if
        self.permission_required is None. Else the permission is generated by the self.action attribute.
        """
        if self.permission_required:
            return super().get_required_permissions(request=request)
        return [self.get_default_permission()]


class GenericGlobalPermissionRequiredMixin(GenericPermissionMixin, DjangoPermissionRequiredMixin):
    raise_exception = True
    action = None

    def get_permission_required(self):
        """return the default view permission of the given model in format: 'app_label.model_name' if
        self.permission_required is None. Else the permission is generated by the self.action attribute.
        """
        if self.permission_required:
            return super().get_permission_required()
        return (self.get_default_permission(), )


class SecuredCreateView(LoginRequiredMixin, GenericGlobalPermissionRequiredMixin, GenericViewContextMixin, InitFormMixin, SuccessMessageDeleteMixin, CreateView):
    """
    Secured django `CreateView` class with default permission '<app_label>.add_<model_name>'
    """
    action = 'add'
    accept_global_perms = True

    def get_required_permissions(self, request=None):
        """return the default view permission of the given model in format: 'app_label.model_name' if
        self.permission_required is None. Else the permission is generated by the self.action attribute.
        """
        if self.permission_required:
            return super().get_required_permissions(request=request)
        return [self.get_default_permission()]

    def get_success_url(self):
        if not self.success_url:
            return reverse_lazy(f'{self.app_label}:{self.model_name}_view', args=[self.object.pk])


class SecuredDetailView(LoginRequiredMixin, GenericPermissionRequiredMixin, GenericViewContextMixin, DetailView):
    """
    Secured django `DetailView` class with default permission '<app_label>.view_<model_name>'
    """
    action = 'view'


class SecuredDeleteView(LoginRequiredMixin, GenericPermissionRequiredMixin, GenericViewContextMixin, SuccessMessageDeleteMixin, DeleteView):
    """
    Secured django `DeleteView` class with default permission '<app_label>.delete_<model_name>'
    """
    action = 'delete'

    def get_success_url(self):
        if not self.success_url:
            return reverse_lazy(f'{self.app_label}:{self.model_name}_overview')


class SecuredUpdateView(LoginRequiredMixin, GenericPermissionRequiredMixin, GenericViewContextMixin, InitFormMixin, SuccessMessageMixin, UpdateView):
    """
    Secured django `UpdateView` class with default permission '<app_label>.change_<model_name>'
    """
    action = 'change'
    template_name = "MrMap/detail_views/generic_form.html"

    def get_success_url(self):
        if not self.success_url:
            return reverse_lazy(f'{self.app_label}:{self.model_name}_view', args=[self.object.pk])


class SecuredListMixin(LoginRequiredMixin, GenericPermissionListMixin, CustomSingleTableMixin):
    """
    Secured django-tables2 table mixin class with default permission '<app_label>.view_<model_name>'
    """
    action = 'view'


class SecuredDependingListMixin(SecuredListMixin, DependingListView):
    """
    Secured `DependingListView` mixin class with default permission '<app_label>.view_<model_name>'
    """


class SecuredConfirmView(LoginRequiredMixin, PermissionRequiredMixin, GenericViewContextMixin, InitFormMixin, SuccessMessageMixin, ConfirmView):
    """
    Secured `ConfirmView` class with default permission '<app_label>.change_<model_name>'
    """
    action = 'change'
