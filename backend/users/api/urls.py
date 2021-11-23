from users.api.views import users as user_views
from users.api.views import groups as group_views
from rest_framework_extensions.routers import ExtendedSimpleRouter

app_name = 'users'

nested_api_router = ExtendedSimpleRouter()
(
    nested_api_router.register(r'users', user_views.MrMapUserViewSet, basename='mrmapuser')
                     .register(r'organizations', group_views.OrganizationViewSet, basename='organization', parents_query_lookups=['user']),
    nested_api_router.register(r'groups', group_views.GroupViewSet, basename='organization'),
    nested_api_router.register(r'organizations', group_views.OrganizationViewSet, basename='organization'),
)

urlpatterns = nested_api_router.urls
