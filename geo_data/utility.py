import IP2Location
import iso3166
import pycountry
from timezonefinder import TimezoneFinder
import requests
database = IP2Location.IP2Location("iplite_database/IP2LOCATION-LITE-DB11.BIN")
asn_database = IP2Location.IP2Location("iplite_database/IP2LOCATION-LITE-ASN.BIN")

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

def get_country_info(country_code):
    url = f"http://api.geonames.org/countryInfoJSON?country={country_code}&username=hardeynuga"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        # print(data)
        if "geonames" in data and data["geonames"]:
            return data["geonames"][0]  # Return the first country match
        else:
            return "No data found for this country code."
    else:
        return f"Error: {response.status_code}"

def get_timezone_name(latitude, longitude):
    """Finds the timezone from latitude and longitude."""
    try:
        # Convert to float in case the values are strings
        latitude = float(latitude)
        longitude = float(longitude)

        # Validate coordinates
        if latitude == 0.0 and longitude == 0.0:
            return "Unknown (Invalid Coordinates: 0.0, 0.0)"

        # Primary timezone lookup
        timezone = tf.timezone_at(lat=latitude, lng=longitude)

        # Fallback method if the primary lookup fails
        if not timezone:
            timezone = tf.closest_timezone_at(lat=latitude, lng=longitude)

        return timezone if timezone else "Unknown (No Matching Timezone)"
    except ValueError:
        return "Unknown (Invalid Coordinate Values)"
    except Exception as e:
        return f"Unknown (Error: {str(e)})"


def get_location_from_ip(ip_address):
    try:
        #Look up the IP address
        response = database.get_all(ip_address)
        asn_response = asn_database.get_all(ip_address)
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
            'timezone': timezone_name,
            'asn': asn_response.asn,
            
        }

        return location_data
    except Exception as e:
        return {'error': str(e)}

