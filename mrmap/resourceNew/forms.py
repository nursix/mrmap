from django import forms
from django.utils.translation import gettext_lazy as _
from MrMap.validators import validate_get_capablities_uri
from resourceNew.enums.service import AuthTypeEnum
from structure.models import Organization


class RegisterServiceForm(forms.Form):
    test_url = forms.URLField(validators=[validate_get_capablities_uri],
                              label=_("Service url"),
                              help_text=_("this shall be the full get capabilities request url."))
    registering_for_organization = forms.ModelChoiceField(
        label=_("Registration for organization"),
        help_text=_("Select for which organization you'd like to register the service."),
        queryset=Organization.objects.none(),
        to_field_name='id',
    )
    username = forms.CharField(max_length=255,
                               required=False,
                               label=_("username"),
                               help_text=_("the username used for the authentication."))
    password = forms.CharField(max_length=500,
                               required=False,
                               label=_("password"),
                               help_text=_("the password used for the authentication."),
                               widget=forms.PasswordInput())
    auth_type = forms.ChoiceField(initial=AuthTypeEnum.NONE.value,
                                  choices=AuthTypeEnum.as_choices(),
                                  label=_("authentication type"),
                                  help_text=_("kind of authentication mechanism shall used."))

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        if not self.request.user.is_anonymous:
            self.fields['registering_for_organization'].queryset = self.request.user.get_publishable_organizations().\
                filter(is_autogenerated=False)
