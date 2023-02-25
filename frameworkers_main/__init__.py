import os
from flask import Flask
from .models import db, insert_questions, insert_options, insert_frameworks
from .app import main

def create_app():
    # create the app
    app = Flask(__name__)
    # configure the SQLite database, relative to the app instance folder
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://jhhsmlfgttdqrd:a03424cbff37ef2d109ae798889b248ce55c2300ac3da0792b4398802f593eb4@ec2-3-211-6-217.compute-1.amazonaws.com:5432/d9ghtq67jeiqsd'
    #"sqlite:///frameworkers.db"
    #postgres://jhhsmlfgttdqrd:a03424cbff37ef2d109ae798889b248ce55c2300ac3da0792b4398802f593eb4@ec2-3-211-6-217.compute-1.amazonaws.com:5432/d9ghtq67jeiqsd    # initialize the app with the extension
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