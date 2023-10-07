import pandas as pd
from io import StringIO
from geolite2 import geolite2
from ip2geotools.databases.noncommercial import DbIpCity
from .distance import returnDistance

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
    ip1 = row_data.get('IP Address 1')
    ip2 = row_data.get('IP Address 2')

    lat1, lon1, lat2, lon2 = None, None, None, None

    if ip1:
        response1 = get_full_details_ip2geotools(ip1)
        row_data['Country1'] = response1['Country']
        row_data['City1'] = response1['City']
        lat1 = response1['Latitude']
        lon1 = response1['Longitude']
        row_data['Latitude1'] = lat1
        row_data['Longitude1'] = lon1

    if ip2 and ip2 != "None":
        response2 = get_full_details_ip2geotools(ip2)
        row_data['Country2'] = response2['Country']
        row_data['City2'] = response2['City']
        lat2 = response2['Latitude']
        lon2 = response2['Longitude']
        row_data['Latitude2'] = lat2
        row_data['Longitude2'] = lon2

    distance = returnDistance(ip1, ip2)
    row_data['distance'] = distance
    if distance > 50:
        row_data['risk'] = "high risk distance"
    else:
        row_data['risk'] = "low risk distance"

    map_html = generate_map(lat1, lon1, lat2, lon2)
    row_data['map_html'] = map_html 

    return row_data

def generate_map(lat1, lon1, lat2=None, lon2=None):
    if lat1 and lon1:
        m = folium.Map(location=[lat1, lon1], zoom_start=10)
        folium.Marker([lat1, lon1], tooltip='IP Address 1').add_to(m)
    if lat2 and lon2:
        if not lat1 and not lon1:
            m = folium.Map(location=[lat2, lon2], zoom_start=10)
        folium.Marker([lat2, lon2], tooltip='IP Address 2').add_to(m)
    
    map_html = m._repr_html_()
    return map_html




# Close the database when the application ends and catch up error if exception
def shutdown_context(exception=None):
    if exception:
        print("ERROR:", exception)
    reader.close()