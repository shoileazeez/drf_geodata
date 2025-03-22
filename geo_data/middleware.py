import requests
import logging
from ipware import get_client_ip
from .utility import get_location_from_ip, get_currency_from_country,get_country_info
from user_agents import parse

logger = logging.getLogger(__name__)

class ClientIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = self.get_client_ip(request)  # Get real client IP
        location_data = get_location_from_ip(ip_address) if ip_address else {}
        device_info = self.get_my_device_info(request)

        # Extract country and fetch currency
        country_code = location_data.get("country_code")
        currency = get_currency_from_country(country_code) if country_code else None
        country_info = get_country_info(country_code) if country_code else None

        # Attach data to request
        request.ip_address = ip_address
        request.location_data = location_data
        request.currency = currency
        request.country_info = country_info
        request.device_info = device_info

        return self.get_response(request)

    def get_client_ip(self, request):
        """Fetches the real public IP address of the request."""
        ip_address, is_routable = get_client_ip(request)

        if not ip_address:
            ip_address = "Unknown IP"
        elif not is_routable:
            ip_address = "Private Network IP"

        return ip_address  # Returning extracted `ip_address`
    
    def get_my_device_info(self,request):
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
        return device_info
