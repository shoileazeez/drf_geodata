from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets  import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET"])
def get_client_ip_auto(request):
    ip_address = getattr(request, "ip_address", "Unknown")
    currency = request.currency
    location_data = request.location_data
    threat_info = request.threat_info

    return Response({
        "client_ip": ip_address,
        "location_data": location_data,
        "currency": currency,
        "threat_info": threat_info,
    })

@api_view(["GET"])
def get_client_location_from_ip(request):
    threat_info  = request.threat_info 
    ip_address = request.ip_address
    return Response({
        "client_ip": ip_address,
        "threat_info" : threat_info
    })



