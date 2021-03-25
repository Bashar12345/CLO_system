
import os
import pymongo
import csv
import pandas as pd
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mail import Mail
# from decouple import config
from flask_login import LoginManager, current_user
# from flask_assets import Environment, Bundle  # bundle custom design
# from webassets import Bundle
# from flask_scss import Scss

from EXAM.configaration import Config
#from EXAM.machine import machine_process

from pymongo import MongoClient
from flask_mongoengine import MongoEngine


# from mongoengine import *

# connect(db='exam', host='localhost', port='27017', username='', password='', authentication_source='admin')

# app = Flask(__name__)
# app.config.from_object(Config)
# app.config.from_object(__name__)
# app.run(debug=True)
# if __name__ == '__main__':
# print ("server started")

'''SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['MONGODB_SETTINGS'] = {
    'db': 'exam',
    'host': 'localhost',
    'port': 27017}
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = config('MAIL')
app.config['MAIL_PASSWORD'] = config('MAIL_PASS')'''

mail = Mail()
# mail.init_app()
nosql = MongoEngine()
# nosql = connect('exam')
# nosql.init_app()
bcrypt = Bcrypt()
login_manager = LoginManager()
# login_manager.init_app(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

def machine_process_data_wrangling():
    #courses= course_model.objects()
    #required_data=required_for_generate.objects()
    #mcq_model=machine_learning_mcq_model.objects()
    connection =MongoClient('localhost',27017)
    mongosql=connection.exam
    required=mongosql.required_for_generate
    mcq_data=mongosql.machine_learning_mcq_model
    required_for_generate=required.find()
    needed_course_code=[]
    data=[]
    for i in required_for_generate:
        needed_course_code.append(i['course_code'])
    for j in needed_course_code:
        mcq=mcq_data.find({"course_code":j})
        data.append(list(mcq))
        print(type(mcq))
    header=["course_title","course_code","lesson","quesCLO","complexity_label","mcq"]
    with open('data.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
    """course_title
    course_code
    course_lessons
    lessons
    quesCLO
    complexity_label
    mcq"""
    #for mcqs in mcq:
        #print(mcqs['mcq'])
    #for corse in courses:
    # print(corse['course_title']) # find fuction get the datas in dictionary 
    #csv_data_dic =  dict()
    #csv_data_dic=[{}]
    print("ami machine")


def create_app(config_class=Config):
    app = Flask(__name__)  # run all package as initial flask app
    app.config.from_object(config_class)
    mail.init_app(app)
    nosql.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    machine_process_data_wrangling()
    # machine=machine_process()
    # Scss(app, static_dir='static', asset_dir='assets')
    from EXAM.main.routes import main
    from EXAM.users.routes import users
    from EXAM.Test_paper.routes import Test_paper
    from EXAM.for_errors.error_handler import errors

    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(Test_paper)
    app.register_blueprint(errors)

    return app
