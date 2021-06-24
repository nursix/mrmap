from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ImproperlyConfigured
from django.http import QueryDict
from django.urls import reverse_lazy, NoReverseMatch
from django.views.generic import DetailView, DeleteView, UpdateView, CreateView
from guardian.mixins import LoginRequiredMixin, PermissionRequiredMixin, PermissionListMixin
from MrMap.views import CustomSingleTableMixin, SuccessMessageDeleteMixin, GenericViewContextMixin, InitFormMixin, \
    ConfirmView, DependingListMixin
from django.contrib.auth.mixins import PermissionRequiredMixin as DjangoPermissionRequiredMixin
from django.utils.translation import gettext_lazy as _
from urllib.parse import urlparse, urlunparse
from django.views.generic import FormView
from breadcrumb.utils import check_path_exists
from main.utils import camel_to_snake


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


class GenericSuccessUrlMixin:
    def get_success_url(self):
        if not self.success_url:
            try:
                url = self.object.get_absolute_url()
            except NoReverseMatch:
                try:
                    url = self.object.get_concrete_table_url()
                except NoReverseMatch:
                    raise ImproperlyConfigured(f'configure success_url or define a default detail view for {self.model_name}')
            return url
        else:
            return self.success_url


class DjangoGenericPermissionRequiredMixin(GenericPermissionMixin, DjangoPermissionRequiredMixin):
    raise_exception = True

    def get_permission_required(self):
        """return the default view permission of the given model in format: 'app_label.model_name' if
        self.permission_required is None. Else the permission is generated by the self.action attribute.
        """
        if not self.permission_required:
            self.permission_required = self.get_default_permission()
        return super().get_permission_required()


class GenericPermissionRequiredMixin(GenericPermissionMixin, PermissionRequiredMixin):
    raise_exception = True

    def get_required_permissions(self, request=None):
        """return the default view permission of the given model in format: 'app_label.model_name' if
        self.permission_required is None. Else the permission is generated by the self.action attribute.
        """
        if self.permission_required:
            return super().get_required_permissions(request=request)
        return [self.get_default_permission()]


class GenericPermissionListMixin(GenericPermissionMixin, PermissionListMixin):

    get_objects_for_user_extra_kwargs = {'accept_global_perms': False}

    def get_required_permissions(self, request=None):
        """return the default view permission of the given model in format: 'app_label.model_name' if
        self.permission_required is None. Else the permission is generated by the self.action attribute.
        """
        if not self.permission_required:
            self.permission_required = self.get_default_permission()
        return super().get_required_permissions(request=request)


class SecuredCreateView(LoginRequiredMixin,
                        GenericSuccessUrlMixin,
                        DjangoGenericPermissionRequiredMixin,
                        GenericViewContextMixin,
                        InitFormMixin,
                        SuccessMessageMixin,
                        CreateView):
    """
    Secured django `CreateView` class with default permission '<app_label>.add_<model_name>'
    """
    action = 'add'
    template_name = 'MrMap/detail_views/generic_form.html'

    def get_success_message(self, cleaned_data):
        if not self.success_message:
            return _("Successfully created %(obj)s") % self.object
        else:
            return super().get_success_message(cleaned_data)

    def get_required_permissions(self, request=None):
        """return the default view permission of the given model in format: 'app_label.model_name' if
        self.permission_required is None. Else the permission is generated by the self.action attribute.
        """
        if self.permission_required:
            return super().get_required_permissions(request=request)
        return [self.get_default_permission()]


class SecuredDetailView(LoginRequiredMixin, GenericPermissionRequiredMixin, GenericViewContextMixin, DetailView):
    """
    Secured django `DetailView` class with default permission '<app_label>.view_<model_name>'
    """
    action = 'view'


class SecuredDeleteView(LoginRequiredMixin,
                        GenericPermissionRequiredMixin,
                        GenericViewContextMixin,
                        SuccessMessageDeleteMixin,
                        DeleteView):
    """
    Secured django `DeleteView` class with default permission '<app_label>.delete_<model_name>'
    """
    action = 'delete'
    template_name = "MrMap/detail_views/delete.html"

    def get_success_message(self):
        if not self.success_message:
            if not hasattr(self, "object"):
                self.object = self.get_object()
            return _("Successfully deleted %(obj)s") % {"obj": self.object}
        else:
            return super().get_success_message()

    def get_success_url(self):
        model_instance = self.model()
        if not self.success_url:
            return reverse_lazy(f'{model_instance._meta.app_label}:{camel_to_snake(model_instance.__class__.__name__)}_list')
        else:
            return super().get_success_url()


class SecuredUpdateView(LoginRequiredMixin,
                        GenericSuccessUrlMixin,
                        GenericPermissionRequiredMixin,
                        GenericViewContextMixin,
                        InitFormMixin,
                        SuccessMessageMixin,
                        UpdateView):
    """
    Secured django `UpdateView` class with default permission '<app_label>.change_<model_name>'
    """
    action = 'change'
    template_name = "MrMap/detail_views/generic_form.html"
    update_query_string = False

    def get_title(self):
        return _("Edit ") + self.get_object().__str__()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"request": self.request})
        return kwargs

    def get_success_message(self, cleaned_data):
        if not self.success_message:
            return _("Successfully updated %(obj)s") % self.object
        else:
            return super().get_success_message(cleaned_data)

    def get_success_url(self):
        last_url = self.request.META.get('HTTP_REFERER')
        (scheme, netloc, path, params, query, fragment) = urlparse(last_url)

        if self.request.path != path and check_path_exists(path):
            if self.update_query_string:
                last_query_dict = QueryDict(query).copy()
                current_query_dict = self.request.GET.copy()
                for key, value in current_query_dict.items():
                    last_query_dict[key] = value
                query = last_query_dict.urlencode()
                last_url = urlunparse((scheme, netloc, path, params, query, fragment))
            return last_url
        return super().get_success_url()


class SecuredFormView(LoginRequiredMixin,
                      GenericSuccessUrlMixin,
                      GenericPermissionRequiredMixin,
                      GenericViewContextMixin,
                      InitFormMixin,
                      SuccessMessageMixin,
                      FormView):
    """
    Secured django `UpdateView` class with default permission '<app_label>.change_<model_name>'
    """
    template_name = "MrMap/detail_views/generic_form.html"

    def get_success_url(self):
        last_url = self.request.META.get('HTTP_REFERER')
        sections = urlparse(last_url)
        if self.request.path != sections.path and check_path_exists(sections.path):
            return last_url
        return super().get_success_url()


class SecuredListMixin(LoginRequiredMixin, GenericPermissionListMixin, CustomSingleTableMixin):
    """
    Secured django-tables2 table mixin class with default permission '<app_label>.view_<model_name>'
    """
    action = 'view'


class SecuredDependingListMixin(LoginRequiredMixin, GenericPermissionListMixin, DependingListMixin, CustomSingleTableMixin):
    """
    Secured `DependingListView` mixin class with default permission '<app_label>.view_<model_name>'
    """
    action = 'view'


class SecuredConfirmView(LoginRequiredMixin, GenericPermissionRequiredMixin, GenericViewContextMixin, InitFormMixin, SuccessMessageMixin, ConfirmView):
    """
    Secured `ConfirmView` class with default permission '<app_label>.change_<model_name>'
    """
    action = 'change'
