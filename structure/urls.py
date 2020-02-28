from django.urls import path
from structure.views import *

app_name = 'structure'
urlpatterns = [
    path('', index, name='index'),

    path('task/<id>', task, name='task'),
    path('task/remove/<id>', remove_task, name='remove-task'),

    path('groups/', groups_index, name='groups-index'),
    path('groups/detail/<id>', detail_group, name='detail-group'),
    path('groups/edit/<id>', edit_group, name='edit-group'),
    path('groups/delete/<id>', remove_group, name='delete-group'),
    path('groups/new/register-form/', new_group, name='new-group'),
    path('groups/publisher/<id>', list_publisher_group, name='publisher-group'),

    path('organizations/', organizations_index, name='organizations-index'),
    path('organizations/detail/<id>', detail_organizations, name='detail-organization'),
    path('organizations/edit/<id>', edit_org, name='edit-organization'),
    path('organizations/delete/<id>', remove_org, name='delete-organization'),
    path('organizations/new/register-form/', new_org, name='new-organization'),
    #path('organizations/list-publish-request/<id>', list_publish_request, name='index-publish-request'),
    path('organizations/publish-request/<id>', publish_request, name='publish-request'),
    path('organizations/toggle-publish-request/<id>', toggle_publish_request, name='toggle-publish-request'),
    path('organizations/remove-publisher/<id>', remove_publisher, name='remove-publisher'),

]

