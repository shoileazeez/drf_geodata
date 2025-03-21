import IP2Location
import iso3166
import pycountry
from timezonefinder import TimezoneFinder
database = IP2Location.IP2Location("iplite_database/IP2LOCATION-LITE-DB11.BIN")
# proxy_db = IP2Location.IP2Location("iplite_database/IP2PROXY-LITE-PX12.BIN")

tf = TimezoneFinder()

def get_currency_from_country(country_code):
    """Fetches currency code based on country code."""
    try:
        country = pycountry.countries.get(alpha_2=country_code.upper())
        if not country:
            return None
        
        # Get country info using iso3166
        country_info = iso3166.countries_by_alpha2.get(country_code.upper())
        if not country_info:
            return None
        
        # Get currency info
        currency = pycountry.currencies.get(numeric=country_info.numeric)
        return currency.alpha_3 if currency else None
    except Exception:
        return None

def get_timezone_name(latitude, longitude):
    """Converts lat/lon to a human-readable timezone name."""
    try:
        timezone = tf.timezone_at(lng=longitude, lat=latitude)
        return timezone if timezone else "Unknown"
    except Exception:
        return "Unknown"

def get_location_from_ip(ip_address):
    try:
        #Look up the IP address
        response = database.get_all(ip_address)
        # try:
        #     proxy_data = proxy_db.get_all(ip_address)
        # except Exception:
        #     proxy_data = None
        # Extract location data
        
        latitude = response.latitude
        longitude = response.longitude
        
        # Convert timezone offset to a human-readable name
        timezone_name = get_timezone_name(latitude, longitude)
        
        location_data = {
            'country_code': response.country_short,
            'country': response.country_long,
            'region': response.region,
            'city': response.city,
            'latitude': response.latitude,
            'longitude': response.longitude,
            'zip_code': response.zipcode,
            'timezone': timezone_name
        }
        
        # if proxy_data:
        #     location_data.update({
        #         "isp": getattr(proxy_data, "isp", "Unknown"),
        #         "asn": getattr(proxy_data, "asn", "Unknown"),
        #         "proxy_type": getattr(proxy_data, "proxy_type", "Unknown"),
        #         "threat": getattr(proxy_data, "threat", "Unknown"),
        #         "fraud_score": getattr(proxy_data, "fraud_score", "Unknown"),
        #         "last_seen": getattr(proxy_data, "last_seen", "Unknown"),
        #         "residential": getattr(proxy_data, "is_residential", False),
        #         "usage_type": getattr(proxy_data, "usage_type", "Unknown"),
        #   })
        return location_data
    except Exception as e:
        return {'error': str(e)}

