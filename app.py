from flask import Flask, render_template, redirect, flash, session
from models import db, connect_db, User
from forms import RegistrationForm, LoginForm


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "soooooooSecretDuh"

connect_db(app)
db.create_all()


@app.route("/")
def index():
    """Index."""

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register_user():
    """Page to register new user."""

    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User(username=username,
                        password=password,
                        email=email,
                        first_name=first_name,
                        last_name=last_name)
        db.session.add(new_user)

        user_credentials = User.register(username, password)
        db.session.add(user_credentials)

        db.session.commit()

        flash(f"Congrats, {first_name}! You have succesfully registered!")
        return redirect("/secret")  # USER'S HOMEPAGE, ONCE LOGGED IN
    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_user():
    """Page for user to login."""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            return redirect("/secret")
        else:
            form.username.errors = ["Incorrect User Name or Password!"]

    return render_template("login.html", form=form)


@app.route("/secret")
def secret():
    """Renders the user's homepage."""

    if "username" not in session:
        # flash("You must login first!")
        return redirect("/")
    else:
        return render_template("secret.html")


@app.route("/logout")
def logout():
    """Logs user out and redirects to home."""

    session.pop("username")

    return redirect("/")
