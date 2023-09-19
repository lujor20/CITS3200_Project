from flask import Blueprint

tool2 = Blueprint('tool2', __name__, template_folder='templates',static_folder='static', static_url_path = '/tool2/static')
