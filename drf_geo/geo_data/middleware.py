import requests
# from .utility import get_location_from_ip
import logging
class ClientIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = requests.get("https://api.ipify.org/?format=json", timeout=5)
            if response.status_code == 200:
                ip_address = response.json().get("ip", "Unknown")
            else:
                ip_address = "Unknown"
        except requests.RequestException:
            ip_address = "Unknown"

        request.ip_address = ip_address
        # request.location_data = get_location_from_ip(ip_address)

        return self.get_response(request)
