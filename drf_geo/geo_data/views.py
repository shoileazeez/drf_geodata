from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets  import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from ipware import get_client_ip
@api_view(["GET"])
def get_client_ip_auto(request):
    ip_address = getattr(request, "ip_address", "Unknown")

    return Response({
        "client_ip": ip_address,
    })

@api_view(["GET"])
def get_client_location_from_ip(request):
    client_location = request.location_data 
    return Response({
        "client_location" : client_location
    })


def my_view(request):
    return JsonResponse({
        "ip_address": request.ip_address,
        "location_data": request.location_data,
    })
from django.http import JsonResponse

def my_view(request):
    client_ip = get_client_ip(request)
    return JsonResponse({'ip': client_ip})
