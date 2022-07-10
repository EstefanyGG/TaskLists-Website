# this file  makes "website code" folder a package
# we can import "website code" folder whatever 
# is in this folder will run automatically once the folder is imported
# set up
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME= "database.db"

def create_app():
    # name of the file ran
    app = Flask(__name__)
    # encrypt/secure cookies/session data
    app.config['SECRET_KEY'] = 'cogito, ergo sum'
    # store database in website folder
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #initialize database by giving it the flask app created
    db.init_app(app)

    # important blueprints
    from .views import views
    # register blueprints, no prefix
    app.register_blueprint(views, url_prefix ='/')

    # define classes, before initializing database
    from .models import User, Task

    create_database(app)

    login_manager = LoginManager()
    # where flask redirects if not logged in
    login_manager.login_view = 'views.login'
    # telling login manager what app we are using
    login_manager.init_app(app)
 
    @login_manager.user_loader
    # telling flask how we load a user, looks by primary key
    def load_user(id):
        return User.query.get(int(id))

    return app

# function to check if data base exists and create it 
def create_database(app):
     if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')