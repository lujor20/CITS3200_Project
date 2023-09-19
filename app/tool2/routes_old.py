from flask import request, render_template, jsonify
import pandas as pd
from io import StringIO
from geolite2 import geolite2

from . import tool2

# Open the database once and keep it open as a global variable
reader = geolite2.reader()

def get_country(ip):
    location = reader.get(ip)
    if location and 'country' in location:
        return location['country']['iso_code']
    return None

@tool2.route('/tool2', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        csv_data = request.data.decode('utf-8')
        data = pd.read_csv(StringIO(csv_data))
        result = data[['Last Edited by: IP Address', 'Username']].copy()

        result['Country'] = result['Last Edited by: IP Address'].apply(get_country)
        filtered_result = result[result['Country'].isin(['AU'])]

        return jsonify(filtered_result.to_dict(orient='records'))

    return render_template("cheating_tool2.html")

# Close the database when the application ends
@tool2.teardown_app_request #changed from teardown_appcontext??
def shutdown_context(exception=None):
    reader.close()