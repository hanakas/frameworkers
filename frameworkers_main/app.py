from flask import Blueprint, render_template, request, redirect, url_for
from .models import Question, Option, Framework

main = Blueprint("main", __name__)

#Create a route decorator 
@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@main.route('/library')
def library():
    return render_template("library.html")

@main.route('/q', methods=['GET', 'POST'])
def q():
    question = Question.query.get(1)
    option = Option
    return render_template("question.html", question=question, option=option)

@main.route('/rsp', methods=['GET', 'POST'])
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
            return redirect(url_for('main.framework', recommendation_id=recommendation))
    if clck == 1:
        if next_q2 > 0:
            question = Question.query.get(next_q2)
            option = Option
            return render_template('question.html', question=question, option=option)
        if framework2 > 0:
            recommendation = Framework.query.get(framework2).id
            return redirect(url_for('main.framework', recommendation_id=recommendation))
    else:
        return "Error"

@main.route('/framework/<recommendation_id>', methods=['GET', 'POST'])
def framework(recommendation_id):
    recommendation = Framework.query.get(recommendation_id)
    return render_template('recommendation.html', recommendation=recommendation)
