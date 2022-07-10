# to store database models
#database for user and tasks
# importing from website file
# Resources flask sql alchemy documentation
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# define model, name object, inherits from db.model
# columns to store
class Task(db.Model):
    # primary key true to make unique
    id = db.Column(db.Integer, primary_key=True)
    #description = db.Column(db.String(200))
    title = db.Column(db.String(50))
    dueDate = db.Column(db.String(50))
    complete = db.Column(db.Boolean, default=False)
    data = db.Column(db.String(10000))
    # default value of field is a function that retrieves time
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # 1 user many tasks == 1 too many relationship 
    # foregin key must recieve valid user id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# user mix in used so that auth.p flask_login current user works
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # length of string, unique true means no 2 users can 
    # have the same email
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # everytime task is created stores here
    # like a list of different tasks relationship with task class
    tasks = db.relationship('Task')
