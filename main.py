from flask import render_template, redirect, url_for, request
from . import db
from . import create_app

app = create_app()

#Create a route decorator 
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/library')
def library():
    return render_template("library.html")

@app.route('/question')
def question():
    # Clears the content of the 'response' table
    #db.session.query(Response).delete()
    #db.session.commit()
    return render_template("question.html")

@app.route('/recommendation')
def recommendation():
    return render_template("recommendation.html")

