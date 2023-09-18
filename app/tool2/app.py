from flask import Flask, request, render_template, jsonify
from IPtoLocation import process_csv_data, shutdown_context, process_detail_data, generate_map
from runDemo.integrated import integrated
from flask import Flask, render_template, send_file
import os


app = Flask(__name__)
# quick ip recognize
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        csv_data = request.data.decode('utf-8')
        processed_data = process_csv_data(csv_data)
        return jsonify(processed_data)
    return render_template("cheating_tool2.html")
# details for click the rows
@app.route('/get_user_details', methods=['POST'])
def get_user_details():
    row_data = request.json
    detailed_data = process_detail_data(row_data)
    map_html = generate_map(detailed_data['Latitude'], detailed_data['Longitude'])
    detailed_data['map'] = map_html
    return jsonify(detailed_data)

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

@app.route('/run_demo', methods=['GET','POST'])
def run_demo():
    file_path = os.path.join('runDemo', 'ipwithflag.csv')
    integrated()
    return send_file(file_path)


if __name__ == '__main__':
    app.run(debug=True)

@app.teardown_appcontext
def handle_teardown(exception=None):
    shutdown_context(exception)
