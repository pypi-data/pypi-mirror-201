from django.urls import path
from . import models, views
from netbox.views.generic import ObjectChangeLogView

urlpatterns = (

    # DeviceSoftware
    path('device-software/', views.DeviceSoftwareListView.as_view(), name='devicesoftware_list'),
    path('device-software/add/', views.DeviceSoftwareEditView.as_view(), name='devicesoftware_add'),
    path('device-software/<int:pk>/', views.DeviceSoftwareView.as_view(), name='devicesoftware'),
    path('device-software/<int:pk>/edit/', views.DeviceSoftwareEditView.as_view(), name='devicesoftware_edit'),
    path('device-software/<int:pk>/delete/', views.DeviceSoftwareDeleteView.as_view(), name='devicesoftware_delete'),
    path('device-software/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='devicesoftware_changelog', kwargs={
        'model': models.DeviceSoftware
    }),   

)
