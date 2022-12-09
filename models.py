from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Questions asked to the user to diagnose their scenario
class Question(db.Model):
    __tablename__ = 'Question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.Text)
    def __repr__(self):
        return f"Question('{self.question}')"

#Available answers to the questions 
class Option(db.Model):
    __tablename__ = 'Option'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    option = db.Column(db.String(200))
    question_id = db.Column(db.Integer, db.ForeignKey('Question.id'), nullable=False)
    next_question_id = db.Column(db.Integer, db.ForeignKey('Question.id'), nullable=False)
    def __repr__(self):
        return f"Option('{self.option}')"

#User's response to the prompts
class Response(db.Model):
    __tablename__ = 'Response'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('Question.id'), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('Option.id'), nullable=False)


#Recommended framework based on the selected options
class Framework(db.Model):
    __tablename__ = 'Framework'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    framework_name = db.Column(db.String(200))
    description = db.Column(db.Text)
    what = db.Column(db.Text)
    how = db.Column(db.Text)
    example = db.Column(db.Text)
    related_framework_1 = db.Column(db.Integer)
    related_framework_2 = db.Column(db.Integer)
    related_framework_3 = db.Column(db.Integer)
    option_id = db.Column(db.Integer, db.ForeignKey('Option.id'), nullable=False)

#Tags of the 5 categories associated with the framework
class Tag(db.Model):
    __tablename__ = 'Tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    framework_id = db.Column(db.Integer, db.ForeignKey('Framework.id'), nullable=False)
    tag_name = db.Column(db.String(200))