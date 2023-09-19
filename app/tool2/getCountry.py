import pandas as pd
from geolite2 import geolite2

csv_data = pd.read_csv("example LMS test log.csv")
result = csv_data[['Last Edited by: IP Address', 'Username']].copy()
reader = geolite2.reader()
def get_country(ip):
    location = reader.get(ip)
    if location and 'country' in location:
        return location['country']['iso_code']
    else:
        return None
result['Country'] = result['Last Edited by: IP Address'].apply(get_country)

unique_countries = result['Country'].unique()
reader.close()
print("Unique countries in the data:", unique_countries)
