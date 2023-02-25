from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    # create the app
    app = Flask(__name__)
    # configure the SQLite database, relative to the app instance folder
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///frameworkers.db"
    # create the extension
    # initialize the app with the extension
    db.init_app(app)
    
    return app
