from app import *
app.app_context().push()
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
from models import *
db.create_all()

