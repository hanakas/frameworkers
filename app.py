import os
from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Float, Date, Table, Integer, String, MetaData
from flask_migrate import Migrate


app = Flask(__name__)

## configure the SQLite database, relative to the app instance folder
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://lbpuesgrgxtroy:c69c3611357041d19bfc89da2f6d757a5296901d40404c7ea29921cc83255672@ec2-54-208-11-146.compute-1.amazonaws.com:5432/dfih8c05rr38m0'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


#Recommended framework based on the selected options
class Framework(db.Model):
    __tablename__ = "Framework"
    id = db.Column(db.Integer, primary_key=True, nullable=True)
    framework_name = db.Column(db.String(200))
    icon = db.Column(db.String(200))
    description = db.Column(db.Text)
    summary = db.Column(db.Text)
    what_resource = db.Column(db.VARCHAR(500))
    how_to_use = db.Column(db.Text)
    application_resource = db.Column(db.VARCHAR(500))
    related_framework_1 = db.Column(db.Integer)
    related_framework_2 = db.Column(db.Integer)
    related_framework_3 = db.Column(db.Integer)
    def __repr__(self):
        return f"Framework('{self.framework_name}')"

#Available answers to the questions 
class Option(db.Model):
    __tablename__ = "Option"
    id = db.Column(db.Integer, primary_key=True)
    option = db.Column(db.String(200))
    next_question_id = db.Column(db.Integer)
    framework_id = db.Column(db.Integer) 
    def __repr__(self):
        return f"Option('{self.option}')"

#Questions asked to the user to diagnose their scenario
class Question(db.Model):
    __tablename__ = "Question"
    id = db.Column(db.Integer, primary_key=True, nullable=True)
    question = db.Column(db.Text)
    option1 = db.Column(db.Integer, db.ForeignKey('Option.id')) 
    option2 = db.Column(db.Integer, db.ForeignKey('Option.id')) 
    def __repr__(self):
        return f"Question('{self.question}')"


@db.event.listens_for(Question.__table__, 'after_create', once=True)
def insert_questions(*args, **kwargs):
    Questions= [[1,'Has your product already been released to a market in any form (i.e. Alpha, Beta, Official release)?', 1, 2],
        [2,'Is the next version of your product currently under development?', 3, 4],
        [3,'Do you have a single solid product idea that you want to develop?', 5, 6],
        [4,'Is your product an infrequent product (=products which customers only use once or twice in their entire user lifetime)?',7,8],
        [5,'Has a sufficient amount of market/user data been collected to conduct data analysis?',9,10],
        [6,'Are you starting to or already developing a product?',11,12],
        [7,'Do you want to generate or screen ideas?',13,14],
        [8,'How would you like to growth hack your product?',15,16],
        [9,"Is there a need for user interviews to understand your product’s market performance?",17,18],
        [10,'Are you satisfied with the allocation of marketing budgets for your product?',19,20],
        [11,'Is there a clear distribution of roles within your team?',21,22],
        [12,'Which stage is your product currently at?',23,24],
        [13,'Would you like to make prototype(s) to test and validate ideas?',25,26],
        [14,'Which aspect would you like to understand your product better?',27,28],
        [15,'Which would you especially like to see an increase for your product?',29,30],
        [16,'Do you need help in setting priorities to the product features/development tasks?',31,32],
        [17,"Do you know what skills/competencies are needed in your team’s product role?",33,34],
        [18,"Are the targeted customers’ needs already identified?",35,36],
        [19,'Do you want to identify a metric for your product? ',37,38],
        [20,'Would you like to assess how satisfied the customers are with the UX of your product?',39,40],
        [21,'Do you have a clear understanding of what features to include for the release?',41,42],
        [22,"Are you confident that your current product/features reflect your customer’s needs?",43,44],
        [23,'Have you already identified the user journey of your product idea?',45,46],
        [24,"Is ‘shipping early to customers’ a priority for your product?",47,48],
        [25,'Is your product developed in a startup or SaaS company?',49,50],
        [26,'Do you want to generate or evaluate a business model?',51,52],
        [27,'Would you like to plan your development process in a long-term (e.g. roadmap) or short-term (e.g. sprint) perspective?',53,54],
        [28,'Would you like to rank the features quantitatively or qualitatively?',55,56],
        [29,'What scope would you like to use the metric with?',57,58],
        [30,'Is there a need to reduce management overhead or speed up the development process?',59,60],
        [31,'Which factor is more important to consider for your product?',61,62],
        [32,'Is it realistically possible to gather all the key/relevant stakeholders of your product (i.e. sales team, investors, etc.) for a discussion?',63,64]]
        
    for i in Questions:
        db.session.add(Question(id=i[0],question=i[1],option1=i[2],option2=i[3]))
        db.session.commit()


@db.event.listens_for(Option.__table__, 'after_create', once=True)
def insert_options(*args, **kwargs):
    id_num = 0
    Options =[['Yes',2,0],['No',3,0],['Yes',4,0],['No',5,0],['Yes',6,0],['No',7,0],['Yes',0,1],['No',8,0],
                ['Yes',9,0],['No',10,0],['Yes',11,0],['No',12,0],['Idea generation',13,0],['Idea screening',0,2],['Data-driven',0,3],['Vision-driven',0,4],['Yes',0,5],
                ['No',14,0],['Yes',15,0],['No',0,6],['Yes',16,0],['No',17,0],['Concept testing',18,0],['Business strategy development',19,0],['Yes',0,7],['No',0,8],
                ['Customer Engagement',0,9],['Customer Satisfaction',20,0],['Acquisition of new customers',0,10],['Usage of product by existing customers',0,11],
                ['Yes',21,0],['No',22,0],['Yes',0,12],['No',0,13],['Yes',23,0],['No',24,0],['Yes',25,0],['No',26,0],['Yes',0,14],['No',0,15],['Yes',27,0],['No',28,0],
                ['Yes',0,23],['No',0,24],['Yes',0,16],['No',0,17],['Yes',0,18],['No',0,19],['Yes',0,20],['No',29,0],['Generate',0,21],['Evaluate',30,0],['Long-term',30,0],['Short-term',0,25],
                ['Quantitatively',31,0],['Qualitatively',32,0],['Individual/Team level',0,26],['Company level',0,27],['Yes',0,28],['No',0,29],['Cost vs benefit',0,30],['Impact on users',0,31],['Yes',0,32],['No',0,33]]
    for i in Options:
        id_num += 1
        db.session.add(Option(id = id_num, option=i[0], next_question_id=i[1], framework_id=i[2]))
    db.session.commit()

@db.event.listens_for(Framework.__table__, 'after_create', once=True)
def insert_frameworks(*args, **kwargs):
    Frameworks =[[1,'ICED Theory', 'iced.svg', 'Fuels growth of infrequent products by mapping and managing the I, C, E, and D dimensions (Infrequency, Control, Engagement, and Distinctiveness).'],
                    [2,'HIPE', 'hipe.svg', 'Evaluates new product ideas and growth opportunities by considering the four factors of Hypothesis, Investment, Precedent, and Experience. '],
                    [3,'DIBB', 'dibb.svg', 'Builds alignment and transparency by starting with the Data, distilling an Insight from the data, presenting a Belief from the insight, and placing a Bet to pursue and test the belief.'],
                    [4,'GLEe', 'glee.svg', 'Helps create the next growth wave by defining a new product focus and phasing.'],
                    [5,'USER', 'user.svg', 'Maximizes product feedback by determining what is worth acting on, what will move the product forward, and what should sit on a shelf.'],
                    [6,'PESO', 'peso.svg', 'Optimizes marketing communications by categorizing media usage to Paid, Earned, Shared, or Owned media.'], 
                    [7,'Design Thinking', 'design.svg', 'Encourages innovation through outlining a phase-based process from empathizing with the users to implementing the product.'],
                    [8,'CIRCLES Method', 'circles.svg', 'Helps evaluate the context, constraints, parameters, and requirements of a product design in a structured manner. '],
                    [9,'DAU / MAU', 'dau.svg', 'Evaluates the engagement level of the users by calculating the the ratio between the Daily Active Users and Monthyl Active Users.'],
                    [10,'AIDA', 'aida.svg', 'Identifies the cognitive stages the user experiences before making a consumer decision through understanding the Attention, Interest, Desire, and Action.'],
                    [11,'Hooked Method', 'hooked.svg', 'Forms user habits by identifying a four-phase loop of trigger, action, variable reward, and investement. '],
                    [12,'DACI', 'daci.svg', "Assigns specific roles to team member in order to improve a team's effectiveness and velocity on projects."], 
                    [13,'Product Team Competencies', 'ptc.svg', "Assesses the team's performance and provides alignment on the focus of the product."],
                    [14,'HEART', 'heart.svg', "Evaluates the user experience (UX) of the product by using five metrics of Happiness, Engagement, Adoption, Retention, and Task success."],
                    [15,'Net Promoter Score', 'nps.svg', "Measures user loyalty and customer satisfaction to the product to evaluate the performance of the product."],
                    [16,'Working Backwards', 'wb.svg', "Drafts a mock press release to conduct a gut-check about a product's viability."],
                    [17,'Customer Journey Map', 'cjm.svg', "Visualizes the stages the users go through when interacting with the product."], 
                    [18,'4D', '4d.svg', "Breaks down the product development into four distinct phases of Discovery, Design, Delivery, and Deduction."],
                    [19,'Jobs To Be Done', 'jtbd.svg', "Identifies the need statements of users by understanding the user's specific goal, or 'job', and the thought processes that would lead them to 'hire' the product to complete the job."],
                    [20,'AARRR Metrics', 'aarrr.svg', "Evaluates user satisfaction through five metrics of Acquisition, Activation, Retention, Referral, and Revenue."],
                    [21,'Lean Canvas', 'lc.svg', "Creates a 1-page business plan by deconstructing the product idea into its key assumptions."],
                    [22,'Ansoff Matrix','am.svg', "Identifies growth opportunity by conceptualizing the level of risk associated with different strategies."],
                    [23,'Opportunity Solution Tree','ost.svg', "Plans the best path to the desired outcome of the product in the ideation/discovery phase by visualizing the opportunities."], 
                    [24,'Quality Function Deployment','qfd.svg', "Translates user needs into technical requirements for the product's development. "],
                    [25,'Eisenhower Matrix','em.svg', "Prioritizes a list of tasks or agenda items by categorizing them according to their urgency and importance."],
                    [26,'OKR','okr.svg', "Formulates outcome-driven goals to ensure team alignment on objectives that matter the most."],
                    [27,'North Star','ns.svg', "Identifies a single, crucial metric that best captures the core value that a product delivers to the users."],
                    [28,'GIST Planning','gist.svg', "Plans the development of the product by breaking down the planning horizon into four parts of Goals, Ideas, Step-projects, and Tasks. "],
                    [29,'666 Roadmap','666.svg', "Outlines a product roadmap over three timelines of the next 6 years, 6 months, and 6 weeks."], 
                    [30,'Weighted Impact Scoring','wis.svg', "Ranks product features on various criteria using a benefit-versus-cost analysis."],
                    [31,'RICE','rice.svg', "Scores the features and intitiatives to determine what to put on roadmaps when developing the product."],
                    [32,'MoSCoW','moscow.svg', "Creates a hierarchy of priorities before and during the project by sorting the requirements in categories of Must have, Should have, Could have, and Will not have."],
                    [33,'Kano Model','kano.svg', "Prioritizes the initiatives according to which features are most likely to delight customers. "]]

    for i in Frameworks:
        db.session.add(Framework(id=i[0],framework_name=i[1], icon=i[2], description=i[3]))
    db.session.commit()

#Create a route decorator 
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/library')
def library():
    framework = Framework
    return render_template("library.html", framework=framework)

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
    icon = recommendation.icon
    return render_template('recommendation.html', recommendation=recommendation, icon=icon)

# with app.app_context():
#     db.drop_all()
#     db.create_all()
    
#     @db.event.listens_for(Question.__table__, 'after_create', once=True)
#     def insert_questions(*args, **kwargs):
#         Questions= [[1,'Has your product already been released to a market in any form (i.e. Alpha, Beta, Official release)?', 1, 2],
#             [2,'Is the next version of your product currently under development?', 3, 4],
#             [3,'Do you have a single solid product idea that you want to develop?', 5, 6],
#             [4,'Is your product an infrequent product (=products which customers only use once or twice in their entire user lifetime)?',7,8],
#             [5,'Has a sufficient amount of market/user data been collected to conduct data analysis?',9,10],
#             [6,'Are you starting to or already developing a product?',11,12],
#             [7,'Do you want to generate or screen ideas?',13,14],
#             [8,'How would you like to growth hack your product?',15,16],
#             [9,"Is there a need for user interviews to understand your product’s market performance?",17,18],
#             [10,'Are you satisfied with the allocation of marketing budgets for your product?',19,20],
#             [11,'Is there a clear distribution of roles within your team?',21,22],
#             [12,'Which stage is your product currently at?',23,24],
#             [13,'Would you like to make prototype(s) to test and validate ideas?',25,26],
#             [14,'Which aspect would you like to understand your product better?',27,28],
#             [15,'Which would you especially like to see an increase for your product?',29,30],
#             [16,'Do you need help in setting priorities to the product features/development tasks?',31,32],
#             [17,"Do you know what skills/competencies are needed in your team’s product role?",33,34],
#             [18,"Are the targeted customers’ needs already identified?",35,36],
#             [19,'Do you want to identify a metric for your product? ',37,38],
#             [20,'Would you like to assess how satisfied the customers are with the UX of your product?',39,40],
#             [21,'Do you have a clear understanding of what features to include for the release?',41,42],
#             [22,"Are you confident that your current product/features reflect your customer’s needs?",43,44],
#             [23,'Have you already identified the user journey of your product idea?',45,46],
#             [24,"Is ‘shipping early to customers’ a priority for your product?",47,48],
#             [25,'Is your product developed in a startup or SaaS company?',49,50],
#             [26,'Do you want to generate or evaluate a business model?',51,52],
#             [27,'Would you like to plan your development process in a long-term (e.g. roadmap) or short-term (e.g. sprint) perspective?',53,54],
#             [28,'Would you like to rank the features quantitatively or qualitatively?',55,56],
#             [29,'What scope would you like to use the metric with?',57,58],
#             [30,'Is there a need to reduce management overhead or speed up the development process?',59,60],
#             [31,'Which factor is more important to consider for your product?',61,62],
#             [32,'Is it realistically possible to gather all the key/relevant stakeholders of your product (i.e. sales team, investors, etc.) for a discussion?',63,64]]
            
#         for i in Questions:
#             db.session.add(Question(id=i[0],question=i[1],option1=i[2],option2=i[3]))
#             db.session.commit()


#     @db.event.listens_for(Option.__table__, 'after_create', once=True)
#     def insert_options(*args, **kwargs):
#         id_num = 0
#         Options =[['Yes',2,0],['No',3,0],['Yes',4,0],['No',5,0],['Yes',6,0],['No',7,0],['Yes',0,1],['No',8,0],
#                     ['Yes',9,0],['No',10,0],['Yes',11,0],['No',12,0],['Idea generation',13,0],['Idea screening',0,2],['Data-driven',0,3],['Vision-driven',0,4],['Yes',0,5],
#                     ['No',14,0],['Yes',15,0],['No',0,6],['Yes',16,0],['No',17,0],['Concept testing',18,0],['Business strategy development',19,0],['Yes',0,7],['No',0,8],
#                     ['Customer Engagement',0,9],['Customer Satisfaction',20,0],['Acquisition of new customers',0,10],['Usage of product by existing customers',0,11],
#                     ['Yes',21,0],['No',22,0],['Yes',0,12],['No',0,13],['Yes',23,0],['No',24,0],['Yes',25,0],['No',26,0],['Yes',0,14],['No',0,15],['Yes',27,0],['No',28,0],
#                     ['Yes',0,23],['No',0,24],['Yes',0,16],['No',0,17],['Yes',0,18],['No',0,19],['Yes',0,20],['No',29,0],['Generate',0,21],['Evaluate',30,0],['Long-term',30,0],['Short-term',0,25],
#                     ['Quantitatively',31,0],['Qualitatively',32,0],['Individual/Team level',0,26],['Company level',0,27],['Yes',0,28],['No',0,29],['Cost vs benefit',0,30],['Impact on users',0,31],['Yes',0,32],['No',0,33]]
#         for i in Options:
#             id_num += 1
#             db.session.add(Option(id = id_num, option=i[0], next_question_id=i[1], framework_id=i[2]))
#         db.session.commit()

#     @db.event.listens_for(Framework.__table__, 'after_create', once=True)
#     def insert_frameworks(*args, **kwargs):
#         Frameworks =[[1,'ICED Theory', 'iced.svg', 'Fuels growth of infrequent products by mapping and managing the I, C, E, and D dimensions (Infrequency, Control, Engagement, and Distinctiveness).'],
#                         [2,'HIPE', 'hipe.svg', 'Evaluates new product ideas and growth opportunities by considering the four factors of Hypothesis, Investment, Precedent, and Experience. '],
#                         [3,'DIBB', 'dibb.svg', 'Builds alignment and transparency by starting with the Data, distilling an Insight from the data, presenting a Belief from the insight, and placing a Bet to pursue and test the belief.'],
#                         [4,'GLEe', 'glee.svg', 'Helps create the next growth wave by defining a new product focus and phasing.'],
#                         [5,'USER', 'user.svg', 'Maximizes product feedback by determining what is worth acting on, what will move the product forward, and what should sit on a shelf.'],
#                         [6,'PESO', 'peso.svg', 'Optimizes marketing communications by categorizing media usage to Paid, Earned, Shared, or Owned media.'], 
#                         [7,'Design Thinking', 'design.svg', 'Encourages innovation through outlining a phase-based process from empathizing with the users to implementing the product.'],
#                         [8,'CIRCLES Method', 'circles.svg', 'Helps evaluate the context, constraints, parameters, and requirements of a product design in a structured manner. '],
#                         [9,'DAU / MAU', 'dau.svg', 'Evaluates the engagement level of the users by calculating the the ratio between the Daily Active Users and Monthyl Active Users.'],
#                         [10,'AIDA', 'aida.svg', 'Identifies the cognitive stages the user experiences before making a consumer decision through understanding the Attention, Interest, Desire, and Action.'],
#                         [11,'Hooked Method', 'hooked.svg', 'Forms user habits by identifying a four-phase loop of trigger, action, variable reward, and investement. '],
#                         [12,'DACI', 'daci.svg', "Assigns specific roles to team member in order to improve a team's effectiveness and velocity on projects."], 
#                         [13,'Product Team Competencies', 'ptc.svg', "Assesses the team's performance and provides alignment on the focus of the product."],
#                         [14,'HEART', 'heart.svg', "Evaluates the user experience (UX) of the product by using five metrics of Happiness, Engagement, Adoption, Retention, and Task success."],
#                         [15,'Net Promoter Score', 'nps.svg', "Measures user loyalty and customer satisfaction to the product to evaluate the performance of the product."],
#                         [16,'Working Backwards', 'wb.svg', "Drafts a mock press release to conduct a gut-check about a product's viability."],
#                         [17,'Customer Journey Map', 'cjm.svg', "Visualizes the stages the users go through when interacting with the product."], 
#                         [18,'4D', '4d.svg', "Breaks down the product development into four distinct phases of Discovery, Design, Delivery, and Deduction."],
#                         [19,'Jobs To Be Done', 'jtbd.svg', "Identifies the need statements of users by understanding the user's specific goal, or 'job', and the thought processes that would lead them to 'hire' the product to complete the job."],
#                         [20,'AARRR Metrics', 'aarrr.svg', "Evaluates user satisfaction through five metrics of Acquisition, Activation, Retention, Referral, and Revenue."],
#                         [21,'Lean Canvas', 'lc.svg', "Creates a 1-page business plan by deconstructing the product idea into its key assumptions."],
#                         [22,'Ansoff Matrix','am.svg', "Identifies growth opportunity by conceptualizing the level of risk associated with different strategies."],
#                         [23,'Opportunity Solution Tree','ost.svg', "Plans the best path to the desired outcome of the product in the ideation/discovery phase by visualizing the opportunities."], 
#                         [24,'Quality Function Deployment','qfd.svg', "Translates user needs into technical requirements for the product's development. "],
#                         [25,'Eisenhower Matrix','em.svg', "Prioritizes a list of tasks or agenda items by categorizing them according to their urgency and importance."],
#                         [26,'OKR','okr.svg', "Formulates outcome-driven goals to ensure team alignment on objectives that matter the most."],
#                         [27,'North Star','ns.svg', "Identifies a single, crucial metric that best captures the core value that a product delivers to the users."],
#                         [28,'GIST Planning','gist.svg', "Plans the development of the product by breaking down the planning horizon into four parts of Goals, Ideas, Step-projects, and Tasks. "],
#                         [29,'666 Roadmap','666.svg', "Outlines a product roadmap over three timelines of the next 6 years, 6 months, and 6 weeks."], 
#                         [30,'Weighted Impact Scoring','wis.svg', "Ranks product features on various criteria using a benefit-versus-cost analysis."],
#                         [31,'RICE','rice.svg', "Scores the features and intitiatives to determine what to put on roadmaps when developing the product."],
#                         [32,'MoSCoW','moscow.svg', "Creates a hierarchy of priorities before and during the project by sorting the requirements in categories of Must have, Should have, Could have, and Will not have."],
#                         [33,'Kano Model','kano.svg', "Prioritizes the initiatives according to which features are most likely to delight customers. "]]

#         for i in Frameworks:
#             db.session.add(Framework(id=i[0],framework_name=i[1], icon=i[2], description=i[3]))
#         db.session.commit()
    
    # insert_frameworks()
    # insert_options()
    # insert_questions()

if __name__=="__main__":
    db.create_all()
    insert_questions()
    insert_options()
    insert_frameworks()
    app.run(debug=True)
