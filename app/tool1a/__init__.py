from flask import Blueprint

tool1a = Blueprint('tool1a', __name__, template_folder='templates', static_folder='static', static_url_path = '/tool1a/static')