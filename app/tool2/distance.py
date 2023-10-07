import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')
warnings.filterwarnings("ignore", category=UserWarning, module='ssl')

import geopy.distance
from ip2geotools.databases.noncommercial import DbIpCity

#
# class for geting precise information on suspiscious ip addresses. reserve or suspiscious ip's
# returns ip address, country code, city, longitude and latitude coordinates
# to use, pass csv of just ip's into file argument
#

def returnDistance(ip_address1, ip_address2):
    # Check if either IP address is empty
    if ip_address2 == 'None':
        return 0

    # Retrieve location details for both IP addresses
    res = DbIpCity.get(ip_address1, api_key="free")
    print(res)
    res2 = DbIpCity.get(ip_address2, api_key="free")
    print(res2)

    if not res.latitude or not res.longitude:
        return None
    if not res2.latitude or not res2.longitude:
        return None

    # Calculate the distance if both results are valid
    coords_1 = (float(res.latitude), float(res.longitude))
    print(coords_1)
    coords_2 = (float(res2.latitude), float(res2.longitude))
    print(coords_2)
    ip_distance = geopy.distance.geodesic(coords_1, coords_2).km
    print(ip_distance)

    # Return the details and distance
    return ip_distance





