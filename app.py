from models import *
from config import Configuration

from flask import Flask
import flask_whooshalchemy as wa
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail
import flask_excel as excel
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://sql:1@localhost/Students2'
db = SQLAlchemy(app)


app.config.from_object(Configuration)

bootstrap = Bootstrap(app)

db.init_app(app)

mail = Mail(app)

excel.init_excel(app)

migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

wa.whoosh_index(app, Student)
wa.whoosh_index(app, Grp)

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


