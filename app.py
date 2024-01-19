import os
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config['SECRET_KEY'] = 'thisisasecretkey'

db = SQLAlchemy(app)

login_manager = LoginManager()  #initialize user authentication session
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader #loads user from database
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin): #User database/class
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return self.id
    

class RegisterForm(FlaskForm): #form for creating a new user
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError('That username already exists. Please choose a different one.')

class LoginForm(FlaskForm): #form for logging in as existing user
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

class Task(db.Model): #database/class for tasks
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tasks', lazy=True))
    taskName = db.Column(db.String(100), nullable=False)
    taskDesc = db.Column(db.Text, nullable=False)

def createTask(taskName, taskDesc): #create a task and use logged in user as user 
    task_obj = Task(user=current_user, taskName=taskName, taskDesc=taskDesc)
    db.session.add(task_obj)
    db.session.commit()

class TaskForm(FlaskForm): #for creating a task
    taskName = StringField("Enter the name of the task: ", validators=[DataRequired()])
    taskDesc = StringField("Enter the task description: ", validators=[DataRequired()])
    submit = SubmitField("Add Task")

with app.app_context(): #create database if not already existing
    db.create_all()

@app.route('/')
def home():
    return render_template('Home.html')


@app.route('/login', methods=['GET', 'POST']) #preparing login template
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard')) #instead of the dashboard have it be home and use jinja to make it so the page appears different when you are logged in
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST']) #preparing dashboard template
@login_required
def dashboard():
    my_tasks = Task.query.filter_by(user_id=current_user.id).all() #load all of a users tasks
    return render_template('dashboard.html', current_user=current_user, my_tasks=my_tasks)


@app.route('/logout', methods=['GET', 'POST']) #logs a user out and takes them to login screen
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@ app.route('/register', methods=['GET', 'POST']) #preparing registration page
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/addTask', methods=['GET', 'POST']) #page for adding a task to dashboard
@login_required
def addTask():
    form = TaskForm()

    if form.validate_on_submit():
        taskName = form.taskName.data
        taskDesc = form.taskDesc.data
        createTask(taskName, taskDesc)
        return redirect(url_for('dashboard'))
    else:
        print(form.errors) #for debugging if the form doesnt submit for some reasond

    return render_template("addTask.html",form=form)

@app.route('/deleteTask/<int:task_id>', methods=['POST']) #deletes a task and sends user back to dashboard, in other words, from the users perspective the page refreshes and the task goes away
@login_required
def deleteTask(task_id):
    task = Task.query.get(task_id) #put id in url so we know what task we are deleting
    print(task)
    db.session.delete(task) #delete task from database
    db.session.commit()
    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    app.run(debug=False)



