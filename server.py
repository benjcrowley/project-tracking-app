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
    # get the user id from the session
    user_id = session.get("user_id")
    # get all the teams for the user
    teams = Team.query.filter_by(user_id=user_id).all()
    #get the count of projects for each team
    for team in teams:
        team.project_count = Project.query.filter_by(team_id=team.id).count()
    

    return render_template("home.html", team_form=team_form, teams=teams)


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


# add a route to add projects
@app.route("/add-project/", methods=["POST"])
def add_project():
    project_form = ProjectForm()
    team_id = session.get("team_id")
    if project_form.validate_on_submit():
        project_name = project_form.project_name.data
        description = project_form.description.data
        completed = project_form.completed.data
        new_project = Project(project_name, completed, team_id, description=description)
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for("team_page", team_id=team_id))
    else:
        print("Form is not valid")
        return redirect(url_for("team_page", team_id=team_id))

# add a route to delete a project from a team
@app.route("/delete-project/<int:project_id>")
def delete_project(project_id):
    team_id = session.get("team_id")
    project = Project.query.get(project_id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for("team_page", team_id=team_id))

# add a route to view a team page that displays all the projects for a team
@app.route("/team/<int:team_id>")
def team_page(team_id):
    project_form = ProjectForm()
    # save the team id in the session
    session["team_id"] = team_id
    # get the team
    team = Team.query.get(team_id)
    # get the projects for the team
    projects = Project.query.filter_by(team_id=team_id).all()
    # get the count of projects for the team
    project_count = Project.query.filter_by(team_id=team_id).count()
    return render_template("team-page.html", team=team, projects=projects, project_count=project_count, project_form=project_form)

# add a route to delete a team
@app.route("/delete-team/<int:team_id>")
def delete_team(team_id):
    team = Team.query.get(team_id)
    # check to see if the team has any projects
    projects = Project.query.filter_by(team_id=team_id).all()
    if projects:
        flash("You cannot delete a team with projects")
        return redirect(url_for("home"))
    else:
        db.session.delete(team)
        db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    connect_to_db(app)
    print("Connected to DB.")
    app.run(debug=True, port=8000)
