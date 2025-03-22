from django.urls import path
from .views import get_client_ip_auto,get_client_location_from_ip,get_my_device_info

urlpatterns = [
    path("get-ip-auto/", get_client_ip_auto, name="get_ip_auto"),
    path("location/", get_client_location_from_ip, name="process"),
    path('device-info/', get_my_device_info, name='device-info'),
]
