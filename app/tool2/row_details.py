import pandas as pd
from io import StringIO
from geolite2 import geolite2
from ip2geotools.databases.noncommercial import DbIpCity

#pip install folium
import folium
from folium.plugins import FloatImage


def generate_map(lon=None, lat=None, ):
    if not lat or not lon:
        raise ValueError("You must provide coordinates")
    
    m = folium.Map(location=[lon, lat], zoom_start=10)
    folium.Marker([lon, lat], tooltip='Selected Location').add_to(m)

    map_html = m._repr_html_()
    return map_html