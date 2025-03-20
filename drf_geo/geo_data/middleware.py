import requests
import logging
from .utility import get_location_from_ip, get_currency_from_country

logger = logging.getLogger(__name__)

class ClientIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = self.get_client_ip()
        location_data = get_location_from_ip(ip_address) if ip_address else {}

        # Extract country and fetch currency
        country_code = location_data.get("country")
        currency = get_currency_from_country(country_code) if country_code else None

        # Get Threat Level
        threat_info = self.check_threat_level(ip_address)

        # Attach data to request
        request.ip_address = ip_address
        request.location_data = location_data
        request.currency = currency
        request.threat_info = threat_info

        return self.get_response(request)

    def get_client_ip(self):
        """Fetches the public IP address of the request."""
        ip_address = "Unknown"  # Default value

        try:
            response = requests.get("https://api.ipify.org/?format=json", timeout=5)
            if response.status_code == 200:
                ip_address = response.json().get("ip", "Unknown")
        except requests.RequestException:
            pass

        return ip_address  # Now explicitly returning `ip_address`

    def check_threat_level(self, ip_address):
        """Checks threat level of an IP using a security API."""
        try:
            response = requests.get(f"https://some-threat-api.com/check?ip={ip_address}", timeout=5)
            if response.status_code == 200:
                return response.json()  # Returns risk score, blacklist status
        except requests.RequestException as e:
            logger.error(f"Threat check failed: {e}")
        return {"error": "Threat API Unreachable"}
