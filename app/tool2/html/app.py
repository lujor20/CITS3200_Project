from flask import Flask, request, render_template, jsonify
import pandas as pd
from io import StringIO
from geolite2 import geolite2

app = Flask(__name__)

# Open the database once and keep it open as a global variable
reader = geolite2.reader()

def get_country(ip):
    location = reader.get(ip)
    if location and 'country' in location:
        return location['country']['iso_code']
    return None

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        csv_data = request.data.decode('utf-8')
        data = pd.read_csv(StringIO(csv_data))
        result = data[['Last Edited by: IP Address', 'Username']].copy()

        result['Country'] = result['Last Edited by: IP Address'].apply(get_country)
        # Will be changed when test finished ('KE', 'CN', 'UA', 'IN', 'PK')
        filtered_result = result[result['Country'].isin(['AU'])]

        return jsonify(filtered_result.to_dict(orient='records'))

    return render_template("cheating_tool2.html")


if __name__ == '__main__':
    app.run(debug=True)

# Close the database when the application ends and catch up error if exception
@app.teardown_appcontext
def shutdown_context(exception=None):
    if exception:
        print("ERROR:",exception)
    reader.close()