from flask import Blueprint

tool1 = Blueprint('tool1', __name__, template_folder='templates', static_folder='static', static_url_path = '/tool1/static')