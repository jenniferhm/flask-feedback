"""Forms for users."""

from wtforms import SelectField, StringField, TextAreaField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Optional


class RegistrationForm(FlaskForm):
    """Form for adding a new user."""

    username = StringField("Create Username", validators=[InputRequired()])
    password = PasswordField("Create Password", validators=[InputRequired()])
    email = StringField("Add Email", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])

class LoginForm(FlaskForm):
    """Form for user login."""

    username = StringField("Create Username", validators=[InputRequired()])
    password = StringField("Create Password", validators=[InputRequired()])
