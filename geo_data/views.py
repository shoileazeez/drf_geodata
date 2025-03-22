from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def get_client_ip_auto(request):
    ip_address = getattr(request, "ip_address", "Unknown")
    currency = request.currency
    location_data = request.location_data
    country_info = request.country_info
    device_info = request.device_info

    return Response({
        "client_ip": ip_address,
        "location_data": {
            "location": location_data,
            "country_info": country_info,
            "currency": currency
        },
        "device_info": device_info,
    })

@api_view(["GET"])
def get_client_location_from_ip(request):
    ip_address = request.ip_address
    return Response({
        "client_ip": ip_address,
    })



