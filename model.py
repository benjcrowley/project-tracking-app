import os
from flask_sqlalchemy import SQLAlchemy

# instantiate the flask_sqlalchemy object and save it to a variable called db
db = SQLAlchemy()

# conncet to the database with a function called connect_to_db that allows a parameter called app which will accept a Flask instance passed in
def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["POSTGRES_URI"]
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

# create a class for users table which will inherit from db.Model, table name will be "users"
class User(db.Model):
    # set the table name to be "user"
    __tablename__ = "users"
    # create a column called id which is the primary key
    id = db.Column(db.Integer, primary_key=True)
    # create a column called username which is a string and must be unique and not null
    username = db.Column(db.String(80), unique=True, nullable=False)
    #create a column called password which is a string and must be not null
    password = db.Column(db.String(80), nullable=False)

    # create a relationship between the users table and the teams table with a db.relationship object called teams that is one to many
    teams = db.relationship("Team", backref="user", lazy=True)

    #add an init method to the class to override the default init method, and allow positional arguments to be passed in
    def __init__(self, username, password):
        # set the username attribute to the username argument passed in
        self.username = username
        # set the password attribute to the password argument passed in
        self.password = password

# creat a team class which will inherit from db.Model, table name will be "teams", this table will have a foreign key to the users table
class Team(db.Model):
    # set the table name to be "team"
    __tablename__ = "teams"
   
    # create a column called id which is the primary key
    id = db.Column(db.Integer, primary_key=True)
    # create a column called team_name which is a string and must be unique and not null
    team_name = db.Column(db.String(80), unique=True, nullable=False)
    # create a column called user_id which is an integer and is a foreign key to the users table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # create a relationship between the teams table and the projects table with a db.relationship object called projects that is one to many
    projects = db.relationship("Project", backref="team", lazy=True)

    #add an init method to the class to override the default init method, and allow positional arguments to be passed in
    def __init__(self, team_name, user_id):
        # set the team_name attribute to the team_name argument passed in
        self.team_name = team_name
        # set the user_id attribute to the user_id argument passed in
        self.user_id = user_id

#create a projects class which will inherit from db.Model, table name will be "projects", this table will have a foreign key to the teams table
class Project(db.Model):
    # set the table name to be "project"
    __tablename__ = "projects"
    # create a column called id which is the primary key
    id = db.Column(db.Integer, primary_key=True)
    # create a column called project_name which is a string and must be unique and not null
    project_name = db.Column(db.String(80), unique=True, nullable=False)
    # create a description column which is a string
    description = db.Column(db.String(80), nullable=True)
    # create a completed column which is a boolean that by default is false and is nullable
    completed = db.Column(db.Boolean, default=False, nullable=True)
    # create a column called team_id which is an integer and is a foreign key to the teams table
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)

    #add an init method to the class to override the default init method, and allow positional arguments to be passed in and nullable arguments to none if not passed in
    def __init__(self, project_name, completed, team_id, **kwargs):
        # set the project_name attribute to the project_name argument passed in
        self.project_name = project_name
        # set the description attribute to the description argument passed in
        if "description" in kwargs:
            self.description = kwargs["description"]
        # set the completed attribute to the completed argument passed in
        self.completed = completed
        # set the team_id attribute to the team_id argument passed in
        self.team_id = team_id



# set up if statement to run the app if this file is run directly and interactively
if __name__ == "__main__":
    # import Flask and create an instance of the Flask class called app
    from flask import Flask
    app = Flask(__name__)
    # connect to the database
    connect_to_db(app)
    print("Connected to DB.")