from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db

app = None
UPLOAD_FOLDER="static/uploads"
def create_app():
    app=Flask(__name__)
    print("starting local development")
    app.config.from_object(LocalDevelopmentConfig)
    app.config["UPLOAD_FOLDER"]=UPLOAD_FOLDER
    db.init_app(app)
    app.app_context().push()
    return app

app=create_app()

from application.controllers import *
from application.api import *

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
