from flask import Flask, request, render_template, jsonify, send_file
from .IPtoLocation import process_csv_data, shutdown_context, process_detail_data, generate_map
import os
from .runDemo import integrated
from . import tool2

# quick ip recognize
@tool2.route('/', methods=['GET','POST'])
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

#@tool2.route('/favicon.ico')
#def favicon():
    #return tool2.send_static_file('favicon.ico')

@tool2.route('/tool2/run_demo', methods=['GET','POST'])
def run_demo():
    file_path = os.path.join('runDemo', 'ipwithflag.csv')
    integrated_instance = integrated.integrated()
    return send_file(file_path)

#@tool2.teardown_appcontext
#def handle_teardown(exception=None):
    #shutdown_context(exception)

#if __name__ == '__main__':
    #app = Flask(__name__)
    #app.register_blueprint(tool2)
    #app.run(debug=True)
