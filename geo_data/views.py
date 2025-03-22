from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets  import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from user_agents import parse

@api_view(["GET"])
def get_client_ip_auto(request):
    ip_address = getattr(request, "ip_address", "Unknown")
    currency = request.currency
    location_data = request.location_data
    country_info = request.country_info

    return Response({
        "client_ip": ip_address,
        "location_data": {
            "location": location_data,
            "country_info": country_info,
            "currency": currency
        },
    })

@api_view(["GET"])
def get_client_location_from_ip(request):
    ip_address = request.ip_address
    return Response({
        "client_ip": ip_address,
    })

@api_view(["GET"])
def get_my_device_info(request):
    user_agent_string = request.headers.get('User-Agent', '')
    user_agent = parse(user_agent_string)

    device_info = {
        "device": user_agent.device.family or "Unknown",
        "browser": user_agent.browser.family or "Unknown",
        "os": user_agent.os.family or "Unknown",
        "is_mobile": user_agent.is_mobile,
        "is_tablet": user_agent.is_tablet,
        "is_pc": user_agent.is_pc,
    }

    return Response(device_info)


