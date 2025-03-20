import IP2Location

database = IP2Location.IP2Location("iplite_database/IP2LOCATION-LITE-DB11.BIN")

def get_location_from_ip(ip_address):
    try:
        # Look up the IP address
        response = database.get_all(ip_address)
        # Extract location data
        location_data = {
            'country_code': response.country_short,
            'country': response.country_long,
            'region': response.region,
            'city': response.city,
            'latitude': response.latitude,
            'longitude': response.longitude,
            'zip_code': response.zipcode,
            'timezone': response.timezone
        }
        return location_data
    except Exception as e:
        return {'error': str(e)}

