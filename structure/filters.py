import django_filters
from django.forms import TextInput, CheckboxInput, ChoiceField, CharField, CheckboxSelectMultiple, BooleanField
from structure.models import Group, Organization


class GroupFilter(django_filters.FilterSet):
    # gsearch = Group search over all method
    gsearch = django_filters.CharFilter(method='filter_search_over_all',
                                        label='Search')

    @staticmethod
    def filter_search_over_all(queryset, name, value):
        dic = list(queryset)
        return queryset.filter(name__icontains=value) | \
               queryset.filter(description__icontains=value) | \
               queryset.filter(organization__organization_name__icontains=value)

    class Meta:
        model = Group
        fields = []


class OrganizationFilter(django_filters.FilterSet):
    # osearch = Organization search over all method
    osearch = django_filters.CharFilter(method='filter_search_over_all',
                                        label='Search')

    # oiag = Organization is_auto_generated
    oiag = django_filters.BooleanFilter(field_name='is_auto_generated',
                                        method='filter_oiag',
                                        widget=CheckboxInput(attrs={'class': 'ml-1'}),
                                        label='Show all organizations'
                                        )

    @staticmethod
    def filter_oiag(queryset, name, value):
        if value:
            q = (queryset.filter(is_auto_generated=True) | queryset.filter(is_auto_generated=False))
        else:
            q = queryset.filter(is_auto_generated=False)
        return q

    @staticmethod
    def filter_search_over_all(queryset, name, value):
        return queryset.filter(organization_name__icontains=value) | \
               queryset.filter(description__icontains=value) | \
               queryset.filter(parent__organization_name__icontains=value)

    class Meta:
        model = Organization
        fields = []
