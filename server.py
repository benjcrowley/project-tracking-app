from flask import Flask, render_template, request, redirect, url_for, flash, session
from forms import TeamForm, ProjectForm, UserForm
from model import db, connect_to_db, Team, Project, User
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

# secret key for CSRF protection
app.secret_key = "secret key"

# instantiate a login form and pass the form into a template
@app.route("/login", methods=["GET", "POST"])
def login():
    user_form = UserForm()
    if user_form.validate_on_submit():
        username = user_form.username.data
        password = user_form.password.data
        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                session["username"] = username
                session["user_id"] = user.id
                flash("Logged in as " + username + "")
                return redirect(url_for("home"))
            else:
                flash("Password is incorrect")
                return redirect(url_for("login"))
        else:
            flash("User does not exist")
            return redirect(url_for("login"))
    else:
        return render_template("login.html", user_form=user_form)

# add a route to logout
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out")
    return redirect(url_for("login"))

# add a route to add users that renders a template to the signup.html
@app.route("/add-user", methods=["GET", "POST"])
def add_user():
    user_form = UserForm()
    if user_form.validate_on_submit():
        username = user_form.username.data
        password = user_form.password.data
        new_user = User(username, password)
        db.session.add(new_user)
        db.session.commit()
        print(new_user)
        flash("User added successfully")
        return redirect(url_for("login"))

    return render_template("signup.html", user_form=user_form)

@app.route("/")
def home():
    # redirect to sign up page if no user is logged in
    if not session.get("username"):
        return redirect(url_for("login"))
    team_form = TeamForm()
    project_form = ProjectForm()
    # get the user id from the session
    user_id = session.get("user_id")
    # get all the teams for the user
    teams = Team.query.filter_by(user_id=user_id).all()
    #get the count of projects for each team
    for team in teams:
        team.project_count = Project.query.filter_by(team_id=team.id).count()
    

    return render_template("home.html", team_form=team_form, project_form=project_form, teams=teams)


# add a route to add teams that have a foreign key to the user
@app.route("/add-team", methods=["POST"])
def add_team():
    team_form = TeamForm()
    if team_form.validate_on_submit():
        team_name = team_form.team_name.data
        user_id = session.get("user_id")
        new_team = Team(team_name, user_id)
        db.session.add(new_team)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        print("Form is not valid")
        return redirect(url_for("home"))


# add a route to add projects that have a foreign key to the team
@app.route("/add-project", methods=["POST"])
def add_project():
    project_form = ProjectForm()
    if project_form.validate_on_submit():
        project_name = project_form.project_name.data
        description = project_form.description.data
        completed = project_form.completed.data
        team_id = project_form.team_id.data
        new_project = Project(project_name, completed, team_id, description=description)
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        print("Form is not valid")
        return redirect(url_for("home"))


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, port=8000)
