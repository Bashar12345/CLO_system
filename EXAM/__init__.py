from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mail import Mail
# from decouple import config
from flask_login import LoginManager, current_user
# from flask_assets import Environment, Bundle  # bundle custom design
# from webassets import Bundle
# from flask_scss import Scss

from EXAM.configaration import Config
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


def create_app(config_class=Config):
    app = Flask(__name__)  # run all package as initial flask app
    app.config.from_object(config_class)
    mail.init_app(app)
    nosql.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
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
