# stores URL endpoints, front end aspects
# stores standard roots
from flask import Flask, Blueprint, render_template, request, flash, jsonify, redirect, url_for 
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import true
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Task
from .models import User
from . import db
import json
from datetime import datetime


views = Blueprint('views', __name__)
# define a root
@views.route('/', methods=['GET', 'POST'])
# can't get to home page unless logged in
@login_required
# this function runs whenever we go to this url
def home():
    # validation to only run this code when the method is post
    if request.method == 'POST':
        # req = request.form
        task = request.form.get('task')
        taskTitle = request.form.get('title')
        due = request.form.get("task-end")   

        if len(task) < 1:
            flash('Must have some task!', category='error')
        else:
            new_task = Task(data=task, title=taskTitle, dueDate=due, user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            flash('Task added!', category='success')
            # checking if the user is authenticated
    return render_template("home.html", user=current_user)

@views.route('/delete-task', methods=['POST'])
def delete_task():
    # take data from post request
    # request.data is a string from .js file
    # taskId turned into python dictionary object
    task = json.loads(request.data)
    taskId = task['taskId']
    # must query before deleting
    task = Task.query.get(taskId)
    if task:
        # delete the object
        db.session.delete(task)
        db.session.commit()
    # returning an empty python dictionary just need to return something
    return jsonify({})

@views.route('/update/<int:task_id>', methods=['GET', 'POST'])
def update(task_id):
    if request.method == 'GET':
        task = db.session.query(Task).filter(Task.id == task_id).first()
        task.complete = not task.complete
        db.session.commit()
    
    return redirect(url_for("views.home"))

#login logout

# to ensure login recieves get and post request
@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        #filters by email and retrieves first search
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    # passing in value to template
    return render_template("login.html", user=current_user)

@views.route('/logout')
# makes sure we can't access page unless user is logged out
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.login'))

@views.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # defining the user from models.py
            # method sha256 is just a hashing algorithm
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            # add to actual database
            db.session.add(new_user)
            # make a commit to database
            db.session.commit()
            #login user after creating account
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            # return redirect 
            # parameters url_for includes name of blueprint.name of function
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

