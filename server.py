from flask import Flask, render_template, request, redirect, url_for, flash
from forms import TeamForm, ProjectForm
from model import db, connect_to_db, Team, Project, User

app = Flask(__name__)

# secret key for CSRF protection
app.secret_key = 'secret key'

@app.route("/")
def home():
    team_form = TeamForm()
    project_form = ProjectForm()
    return render_template("home.html", team_form=team_form, project_form=project_form)

@app.route("/add-team", methods=["POST"])
def add_team():
    team_form = TeamForm()
    if team_form.validate_on_submit():
        team_name = team_form.team_name.data
        print(team_name)
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
        print(project_name, description, completed, team_id)
        return redirect(url_for("home"))
    else:
        print("Form is not valid")
        return redirect(url_for("home"))
    

if __name__ == "__main__":
    app.run(debug=True, port=8000)