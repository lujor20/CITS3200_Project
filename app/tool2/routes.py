from flask import Flask, request, render_template, jsonify, send_file
from .IPtoLocation import process_csv_data, shutdown_context, process_detail_data, generate_map
import os
from .runDemo import integrated
from . import tool2

from pathlib import Path

# quick ip recognize
@tool2.route('/tool2', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        csv_data = request.data.decode('utf-8')
        processed_data = process_csv_data(csv_data)
        return jsonify(processed_data)
    return render_template("cheating_tool2.html")

# details for click the rows
@tool2.route('/get_user_details', methods=['POST'])
def get_user_details():
    row_data = request.json
    detailed_data = process_detail_data(row_data)
    map_html = generate_map(detailed_data['Latitude'], detailed_data['Longitude'])
    detailed_data['map'] = map_html
    return jsonify(detailed_data)

@tool2.route('/run_demo', methods=['GET','POST'])
def run_demo():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, 'runDemo/ipwithflag.csv')
    integrated_instance = integrated.integrated()
    print("This is reading this file ", file_path)
    
    result_file = Path(file_path)
    if result_file.is_file():
        print("It exist")
    return send_file(file_path)


