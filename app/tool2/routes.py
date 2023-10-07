from flask import Flask, request, render_template, jsonify, send_file
from .IPtoLocation import  shutdown_context, process_detail_data, generate_map
import csv
import os
from . import tool2
from .unique_user import cleanfile

from pathlib import Path

# quick ip recognize
@tool2.route('/tool2', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        csv_data = request.data.decode('utf-8')
        # transport drop data 
        with open('temp.csv', 'w', encoding='utf-8') as temp_csv:
            temp_csv.write(csv_data)
        # clean data with formate user,ip1,ip2
        cleanfile('temp.csv')

        # read the cleaned data to send it back to frontend
        cleaned_data_list = []
        with open('Cleaned.csv', 'r', encoding='utf-8') as cleaned_file:
            reader = csv.DictReader(cleaned_file)
            for row in reader:
                cleaned_data_list.append(row)
            return jsonify(cleaned_data_list)
        
    return render_template("cheating_tool2.html")

# details for click the rows
@tool2.route('/get_user_details', methods=['GET', 'POST'])
def get_user_details():
    row_data = request.json
    detailed_data = process_detail_data(row_data)
    return jsonify(detailed_data)

