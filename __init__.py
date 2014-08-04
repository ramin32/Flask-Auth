from flask.ext.login import (LoginManager, login_required, login_user, 
                             logout_user, UserMixin, current_user)
from wtforms import Form, TextField, PasswordField
from wtforms.validators import Required, Required, ValidationError
from flask import Blueprint, request, render_template, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import db

auth = Blueprint('auth', __name__, template_folder='templates')

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = "danger"

    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class LoginForm(Form):
    username = TextField(validators=[Required()])
    password = PasswordField(validators=[Required()])

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    password_hash = db.Column(db.Text)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def authenticate_user(cls, username, password):
        user = cls.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None



@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated():
        return redirect(request.args.get("next") or url_for("index"))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.authenticate_user(form.username.data, form.password.data)
        if user: 
            login_user(user)
            flash("Logged in successfully.", 'success')
            return redirect(request.args.get("next") or url_for("index"))
        flash('Account not found.', 'danger')
    return render_template("login.html", form=form)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))




