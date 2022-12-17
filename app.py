from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

app = Flask(__name__)
SECRET_KEY = "secret"
app.config["SECRET_KEY"] = SECRET_KEY
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:postgres@localhost:5432/postgres"
# 1. add boiler plate code
# 2. need a user class with an id variable
# 3. user loader -> function that takes in a user id and gives back the user object, or none if the user doesn't exist
# 4. call the login_user function on the user object
# 5. if you want to restrict access to a route, use the @login_required decorator

# boiler plate code
login_manager = LoginManager()
login_manager.init_app(app)

# make our user class
class User(userMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("login_page"))


db = SQLAlchemy(app)


class LoginInfo(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


@app.route("/")
@login_required
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET"])
def login_page():
    form = LoginInfo()
    return render_template("login.html", form=form)


@app.route("/signup", methods=["GET"])
def signup_page():
    return render_template("signup.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    result = User.query.filter_by(username=username, password=password).first()
    if result:
        login_user(result)
        return redirect(url_for("secrets"))
    else:
        flash("Username or password is incorrect")
        return redirect(url_for("login_page"))


@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    password = request.form["password"]
    result = User.query.filter_by(username=username).first()
    if result:
        flash("Username already exists")
        return redirect(url_for("signup_page"))
    else:
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("login_page"))
