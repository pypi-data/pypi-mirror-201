from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'netbox_software'

router = NetBoxRouter()
router.register('device-softwares', views.DeviceSoftwareViewSet)

urlpatterns = router.urls
