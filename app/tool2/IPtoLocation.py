import pandas as pd
from io import StringIO
from geolite2 import geolite2
from ip2geotools.databases.noncommercial import DbIpCity

#pip install folium
import folium
from folium.plugins import FloatImage

# Open the database once and keep it open as a global variable
reader = geolite2.reader()

# get country name by geolite
def get_country_geolite(ip):
    location = reader.get(ip)
    if location and 'country' in location:
        return location['country']['iso_code']
    return None

# get country name by ip2geotools
def get_country_ip2geotools(ip):
    try:
        response = DbIpCity.get(ip, api_key='free')
        return response.country
    except:
        return None

# get country name
def get_country(ip):
    country = get_country_geolite(ip)
    if country is None:
        country = get_country_ip2geotools(ip)
    return country

# get flag
def get_location_type(country):
    if country == 'AU':
        return 'DOMESTIC'
    elif country in ["KE", "PK", "IN", "MA", "UA", "CN"]:
        return 'SUSPICIOUS'
    else:
        return 'INTERNATIONAL'
def process_csv_data(csv_data):
    data = pd.read_csv(StringIO(csv_data))
    result = data[['Last Edited by: IP Address', 'Username']].copy()
    result['Country'] = result['Last Edited by: IP Address'].apply(get_country)

    # Create a new column to specify if the country is DOMESTIC or INTERNATIONAL
    result['Flag'] = result['Country'].apply(get_location_type)

    return result.to_dict(orient='records')

def get_full_details_ip2geotools(ip):
    """
    This function returns full details using the DbIpCity module.
    """
    try:
        response = DbIpCity.get(ip, api_key='free')
        return {
            "IP": ip,
            "Country": response.country,
            "City": response.city,
            "Latitude": response.latitude,
            "Longitude": response.longitude
        }
    except:
        return {
            "IP": ip,
            "Country": None,
            "City": None,
            "Latitude": None,
            "Longitude": None
        }

def process_detail_data(row_data):
    """
    Process the row data to add latitude and longitude details.
    Args:
    - row_data: A dictionary containing at least 'Username' and 'Last Edited by: IP Address'
    Returns:
    - A dictionary with added latitude and longitude details.
    """
    ip = row_data.get('Last Edited by: IP Address')
    response = get_full_details_ip2geotools(ip)

    # Update the original row data with new details
    row_data['Latitude'] = response['Latitude']
    row_data['Longitude'] = response['Longitude']
    row_data['Country'] = response['Country']
    row_data['City'] = response['City']

    map_html = generate_map(response['Latitude'], response['Longitude'])
    row_data['map_html'] = map_html

    return row_data

def generate_map(latitude, longitude):
    m = folium.Map(location=[latitude, longitude], zoom_start=15)
    folium.Marker([latitude, longitude]).add_to(m)

    map_html = m._repr_html_()
    return map_html


# Close the database when the application ends and catch up error if exception
def shutdown_context(exception=None):
    if exception:
        print("ERROR:", exception)
    reader.close()