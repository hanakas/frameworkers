import os
from flask import Flask
from .models import db, insert_questions, insert_options, insert_frameworks
from .app import main

def create_app():
    # create the app
    app = Flask(__name__)
    # configure the SQLite database, relative to the app instance folder
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///frameworkers.db"
    #"sqlite:///frameworkers.db"
    #postgresql://frameworkers_user:MBdkxqxBZZuQgYXLhXVMuiGPE16ahw04@dpg-cft605pa6gdotcdifh7g-a.oregon-postgres.render.com/frameworkers
    # initialize the app with the extension
    app.register_blueprint(main)
    app.debug = False
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()
        insert_questions()
        insert_options()
        insert_frameworks()
    return app