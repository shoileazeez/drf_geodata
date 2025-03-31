from django.urls import path

from .views import get_client_ip_auto, get_client_location_from_ip, UserRegistrationView

urlpatterns = [
    path("get-ip-auto/", get_client_location_from_ip, name="get_ip_auto"),
    path("location/", get_client_ip_auto, name="process"),
    path("register/", UserRegistrationView.as_view(), name="register")
]
