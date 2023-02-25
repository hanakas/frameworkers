import os
from flask import Flask
from flask import render_template, request, redirect, url_for
from models import db, Question, Option, Framework,insert_questions, insert_options, insert_frameworks

app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://jhhsmlfgttdqrd:a03424cbff37ef2d109ae798889b248ce55c2300ac3da0792b4398802f593eb4@ec2-3-211-6-217.compute-1.amazonaws.com:5432/d9ghtq67jeiqsd'
#"sqlite:///frameworkers.db"
#postgres://jhhsmlfgttdqrd:a03424cbff37ef2d109ae798889b248ce55c2300ac3da0792b4398802f593eb4@ec2-3-211-6-217.compute-1.amazonaws.com:5432/d9ghtq67jeiqsd    # initialize the app with the extension
app.debug = False
db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()
    insert_questions()
    insert_options()
    insert_frameworks()

#Create a route decorator 
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/library')
def library():
    return render_template("library.html")

@app.route('/q', methods=['GET', 'POST'])
def q():
    question = Question.query.get(1)
    option = Option
    return render_template("question.html", question=question, option=option)

@app.route('/rsp', methods=['GET', 'POST'])
def response():
    clck = int(request.form['clck'])
    next_q1 = int(request.form['next_q1'])
    next_q2 = int(request.form['next_q2'])
    framework1 = int(request.form['framework1'])
    framework2 = int(request.form['framework2'])

    if clck == 0:
        if next_q1 > 0:
            question = Question.query.get(next_q1)
            option = Option
            return render_template('question.html', question=question, option=option)
        if framework1 > 0:
            recommendation = Framework.query.get(framework1).id
            return redirect(url_for('framework', recommendation_id=recommendation))
    if clck == 1:
        if next_q2 > 0:
            question = Question.query.get(next_q2)
            option = Option
            return render_template('question.html', question=question, option=option)
        if framework2 > 0:
            recommendation = Framework.query.get(framework2).id
            return redirect(url_for('framework', recommendation_id=recommendation))
    else:
        return "Error"

@app.route('/framework/<recommendation_id>', methods=['GET', 'POST'])
def framework(recommendation_id):
    recommendation = Framework.query.get(recommendation_id)
    return render_template('recommendation.html', recommendation=recommendation)