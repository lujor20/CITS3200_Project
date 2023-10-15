from flask import request, render_template, jsonify, send_file
from .row_details import generate_map
import csv
from . import tool2
from .tool2Final.integrated import integrated


@tool2.route('/tool2', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        csv_data = request.data.decode('utf-8')
        # transport drop data 
        with open('testLog.csv', 'w', encoding='utf-8') as temp_csv:
            temp_csv.write(csv_data)

        integrated('testLog.csv', "initial")

        # read the cleaned data to send it back to frontend
        initial_list = []
        headers = []
        with open('output.csv', 'r', encoding='utf-8') as initial_file:
            reader = csv.DictReader(initial_file)
            headers = reader.fieldnames
            for row in reader:
                initial_list.append(row)

            return jsonify({"headers": headers, "data": initial_list})
        
    return render_template("cheating_tool2.html")

@tool2.route('/international_analysis', methods=['GET','POST'])
def international_analysis():
    if request.method == 'POST':
        csv_data = request.data.decode('utf-8')
        # transport drop data 
        with open('testLog.csv', 'w', encoding='utf-8') as temp_csv:
            temp_csv.write(csv_data)

        integrated('testLog.csv', "international")

        # read the cleaned data to send it back to frontend
        international_list = []
        headers = []
        with open('output.csv', 'r', encoding='utf-8') as international_file:
            reader = csv.DictReader(international_file)
            headers = reader.fieldnames
            for row in reader:
                international_list.append(row)

            return jsonify({"headers": headers, "data": international_list})
        
    return render_template("cheating_tool2.html")

@tool2.route('/distance_analysis', methods=['GET','POST'])
def distance_analysis():
    if request.method == 'POST':
        csv_data = request.data.decode('utf-8')
        with open('duplicate.csv', 'w', encoding='utf-8') as temp_csv:
            temp_csv.write(csv_data)

        integrated("testLog.csv", "distance")

        # read the cleaned data to send it back to frontend
        distance_list = []
        headers = []
        with open('output.csv', 'r', encoding='utf-8') as distance_file:
            reader = csv.DictReader(distance_file)
            headers = reader.fieldnames
            for row in reader:
                distance_list.append(row)

            return jsonify({"headers": headers, "data": distance_list})
        
    return render_template("cheating_tool2.html")
        

# details for click the rows
@tool2.route('/get_user_details', methods=['GET', 'POST'])
def get_user_details():
    row_data = request.json
    longitude = float(row_data['longitude'])
    latitude = float(row_data['latitude'])

    map = generate_map(longitude, latitude)
    return jsonify({'id': row_data['id'], 'map_html': map})



# download
@tool2.route('/download')
def download_file():
    path_to_file = "../output.csv"
    return send_file(path_to_file, as_attachment=True, download_name='output.csv')


