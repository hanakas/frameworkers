from flask import render_template, request, redirect, url_for
from . import create_app
from .models import Question, Option, Framework

app = create_app()
app.secret_key = 'mysecretkey'

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
            #return render_template('recommendation.html', recommendation=recommendation)
    if clck == 1:
        if next_q2 > 0:
            question = Question.query.get(next_q2)
            option = Option
            return render_template('question.html', question=question, option=option)
        if framework2 > 0:
            recommendation = Framework.query.get(framework2).id
            return redirect(url_for('framework', recommendation_id=recommendation))
            #return render_template('recommendation.html', recommendation=recommendation)
    else:
        return "Error"

@app.route('/framework/<recommendation_id>', methods=['GET', 'POST'])
def framework(recommendation_id):
    recommendation = Framework.query.get(recommendation_id)
    return render_template('recommendation.html', recommendation=recommendation)