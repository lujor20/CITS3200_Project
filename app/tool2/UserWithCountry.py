import pandas as pd
from geolite2 import geolite2

# load csv data
data = pd.read_csv("example LMS test log.csv")

# get the IP Address and Username columns
result = data[['Last Edited by: IP Address', 'Username']].copy()

# create the reader
reader = geolite2.reader()

# get country name from IP address
def get_country(ip):
    location = reader.get(ip)
    if location and 'country' in location:
        return location['country']['iso_code']
    else:
        return None

# apply the function to the IP Address column and add a new column for the country
result['Country'] = result['Last Edited by: IP Address'].apply(get_country)

# close the reader
reader.close()

# filter the data, only show rows where the country is Kenya, China, Ukraine, India, or Pakistan
# 'KE', 'CN', 'UA', 'IN', 'PK'

filtered_result = result[result['Country'].isin(['AU'])]

print(filtered_result)
