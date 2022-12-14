from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length

class TeamForm(FlaskForm):
    team_name = StringField("team name", validators=[DataRequired(), Length(min=2, max=255)])
    submit = SubmitField("Submit")

class ProjectForm(FlaskForm):
    project_name = StringField("project name", validators=[DataRequired(), Length(min=2, max=255)])
    # add a description field that is not required
    description = StringField("description", validators=[Length(min=2, max=255)])
    # add a completed field that is a boolean True or False and required
    completed = BooleanField("completed")
    # add a team_id field that is an integer and required
    team_id = StringField("team id", validators=[DataRequired()])
    submit = SubmitField("Submit")