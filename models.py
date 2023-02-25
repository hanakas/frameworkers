from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Float, Date, Table, Integer, String, MetaData, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from . import create_app, db

app = create_app()
app.secret_key = 'mysecretkey'

#Recommended framework based on the selected options
class Framework(db.Model):
    __tablename__ = 'Framework'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    framework_name = db.Column(db.String(200))
    # description = db.Column(db.Text)
    # what = db.Column(db.Text)
    # how = db.Column(db.Text)
    # example = db.Column(db.Text)
    # related_framework_1 = db.Column(db.Integer)
    # related_framework_2 = db.Column(db.Integer)
    # related_framework_3 = db.Column(db.Integer)

#Questions asked to the user to diagnose their scenario
class Question(db.Model):
    __tablename__ = 'Question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.Text)
    option1 = db.Column(db.Integer, db.ForeignKey('Option.id')) 
    option2 = db.Column(db.Integer, db.ForeignKey('Option.id')) 
    def __repr__(self):
        return f"Question('{self.question}')"

#Available answers to the questions 
class Option(db.Model):
    __tablename__ = 'Option'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    option = db.Column(db.String(200))
    next_question_id = db.Column(db.Integer, db.ForeignKey('Question.id'))
    framework_id = db.Column(db.Integer, db.ForeignKey('Framework.id')) 
    def __repr__(self):
        return f"Option('{self.option}')"

with app.app_context():
    db.drop_all()
    db.create_all()

    @db.event.listens_for(Question.__table__, 'after_create', once=True)
    def insert_questions(*args, **kwargs):
        Questions= [['Has your product already been released to a market in any form (i.e. Alpha, Beta, Official release)?', 1, 2],
        ['Is the next version of your product currently under development?', 3, 4],
        ['Do you have a single solid product idea that you want to develop?', 5, 6],
        ['Is your product an infrequent product (=products which customers only use once or twice in their entire user lifetime)?',7,8],
        ['Has a sufficient amount of market/user data been collected to conduct data analysis?',9,10],
        ['Are you starting to or already developing a product?',11,12],
        ['Do you want to generate or screen ideas?',13,14],
        ['How would you like to growth hack your product?',15,16],
        ["Is there a need for user interviews to understand your product’s market performance?",17,18],
        ['Are you satisfied with the allocation of marketing budgets for your product?',19,20],
        ['Is there a clear distribution of roles within your team?',21,22],
        ['Which stage is your product currently at?',23,24],
        ['Would you like to make prototype(s) to test and validate ideas?',25,26],
        ['Which aspect would you like to understand your product better?',27,28],
        ['Which would you especially like to see an increase for your product?',29,30],
        ['Do you need help in setting priorities to the product features/development tasks?',31,32],
        ["Do you know what skills/competencies are needed in your team’s product role?",33,34],
        ["Are the targeted customers’ needs already identified?",35,36],
        ['Do you want to identify a metric for your product? ',37,38],
        ['Would you like to assess how satisfied the customers are with the UX of your product?',39,40],
        ['Do you have a clear understanding of what features to include for the release?',41,42],
        ["Are you confident that your current product/features reflect your customer’s needs?",43,44],
        ['Have you already identified the user journey of your product idea?',45,46],
        ["Is ‘shipping early to customers’ a priority for your product?",47,48],
        ['Is your product developed in a startup or SaaS company?',49,50],
        ['Do you want to generate or evaluate a business model?',51,52],
        ['Would you like to plan your development process in a long-term (e.g. roadmap) or short-term (e.g. sprint) perspective?',53,54],
        ['Would you like to rank the features quantitatively or qualitatively?',55,56],
        ['What scope would you like to use the metric with?',57,58],
        ['Is there a need to reduce management overhead or speed up the development process?',59,60],
        ['Which factor is more important to consider for your product?',61,62],
        ['Is it realistically possible to gather all the key/relevant stakeholders of your product (i.e. sales team, investors, etc.) for a discussion?',63,64]]
        
        for i in Questions:
            db.session.add(Question(question=i[0],option1=i[1], option2=i[2]))
        db.session.commit()
    

    @db.event.listens_for(Option.__table__, 'after_create', once=True)
    def insert_options(*args, **kwargs):
        Options =[['Yes',2,0],['No',3,0],['Yes',4,0],['No',5,0],['Yes',6,0],['No',7,0],['Yes',0,1],['No',8,0],
                  ['Yes',9,0],['No',10,0],['Yes',11,0],['No',12,0],['Idea generation',13,0],['Idea screening',0,2],['Data-driven',0,3],['Vision-driven',0,4],['Yes',0,5],
                  ['No',14,0],['Yes',15,0],['No',0,6],['Yes',16,0],['No',17,0],['Concept testing',18,0],['Business strategy development',19,0],['Yes',0,7],['No',0,8],
                  ['Customer Engagement',0,9],['Customer Satisfaction',20,0],['Acquisition of new customers',0,10],['Usage of product by existing customers',0,11],
                  ['Yes',21,0],['No',22,0],['Yes',0,12],['No',0,13],['Yes',23,0],['No',24,0],['Yes',25,0],['No',26,0],['Yes',0,14],['No',0,15],['Yes',27,0],['No',28,0],
                  ['Yes',0,23],['No',0,24],['Yes',0,16],['No',0,17],['Yes',0,18],['No',0,19],['Yes',0,20],['No',29,0],['Generate',0,21],['Evaluate',30,0],['Long-term',30,0],['Short-term',0,25],
                  ['Quantitatively',31,0],['Qualitatively',32,0],['Individual/Team level',0,26],['Company level',0,27],['Yes',0,28],['No',0,29],['Cost vs benefit',0,30],['Impact on users',0,31],['Yes',0,32],['No',0,33]]

        for i in Options:
            db.session.add(Option(option=i[0], next_question_id=i[1], framework_id=i[2]))
        db.session.commit()
    
    @db.event.listens_for(Framework.__table__, 'after_create', once=True)
    def insert_frameworks(*args, **kwargs):
        Frameworks =[['ICED Theory'],
                     ['HIPE'],
                     ['DIBB'],
                     ['GLEe'],
                     ['USER'],
                     ['PESO'], 
                     ['Design Thinking'],
                     ['CIRCLES Method'],
                     ['DAU / MAU'],
                     ['AIDA'],
                     ['Hooked Method'],
                     ['DACI'], 
                     ['Product Team Competencies'],
                     ['HEART'],
                     ['NPS'],
                     ['Working Backwards'],
                     ['Customer Journey Map'], 
                     ['4D'],
                     ['JTBD'],
                     ['AARRR Metrics'],
                     ['Lean Canvas'],
                     ['Ansoff Matrix'],
                     ['Opportunity Solution Tree (OST)'], 
                     ['QFD'],
                     ['Eisenhower Matrix'],
                     ['OKR'],
                     ['North Star'],
                     ['GIST Planning'],
                     ['666 Roadmap'], 
                     ['Weighted Impact Scoring'],
                     ['RICE'],
                     ['MoSCoW'],
                     ['Kano Model']]

        for i in Frameworks:
            db.session.add(Framework(framework_name=i[0]))
        db.session.commit()

    insert_questions()
    insert_options()
    insert_frameworks()