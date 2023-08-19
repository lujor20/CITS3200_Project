import os

from flask import Flask

UPLOAD_FOLDER = "/temp"
ALLOWED_EXTENSIONS = {'.docx'}
SECRET_KEY = os.urandom(32)


def create_app(debug=False):
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SECRET_KEY'] = SECRET_KEY
    app.debug = debug

    # import from "main" folder.
    from app.tool1 import tool1 as tool1_blueprint
    from app.tool1 import routes

    app.register_blueprint(tool1_blueprint)

    return app