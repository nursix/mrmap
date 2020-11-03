"""
Author: Jan Suleiman
Organization: terrestris GmbH & Co. KG
Contact: suleiman@terrestris.de
Created on: 27.10.20

"""
from django.urls import path

from . import views

urlpatterns = [
    path('<int:config_id>/<str:metadata_id>', views.check, name='check'),
]
