from flask import Flask, render_template, redirect, flash, session
from models import db, connect_db, User, Feedback
from forms import RegistrationForm, LoginForm, FeedbackForm


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

    if "username" in session:
        username = session["username"]
        user_info = User.query.get_or_404(username)
        return redirect(f"/users/{user_info.username}")
    else:
        return redirect("/register")

# REGISTER NEW USER
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

        new_user = User.register(username=username,
                                 password=password,
                                 email=email,
                                 first_name=first_name,
                                 last_name=last_name)
        db.session.add(new_user)

        db.session.commit()

        session["username"] = new_user.username

        flash(f"Congrats, {first_name}! You have succesfully registered!")
        # USER'S HOMEPAGE, ONCE LOGGED IN
        return redirect(f"/users/{new_user.username}")
    else:
        return render_template("register.html", form=form)

# USER LOGIN
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
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Incorrect User Name or Password!"]

    return render_template("login.html", form=form)

# USER HOMEPAGE
@app.route("/users/<username>")
def user_page(username):
    """ displays user's homepage. """

    if "username" not in session:
        flash("You must login first!")
        return redirect("/")  # REDIRECT TO LOGIN PAGE
    else:
        user_info = User.query.get_or_404(username)
        return render_template("user.html", user_info=user_info)

# LOGOUT
@app.route("/logout")
def logout():
    """Logs user out and redirects to home."""

    session.pop("username")

    return redirect("/")

# DELETE USER
@app.route("/users/<username>/delete")
def delete_user(username):
    """ deletes a user. """

    if "username" not in session:
        flash("You must login first!")
        return redirect("/")
    else:
        if session["username"] == username:
            user_info = User.query.get_or_404(username)
            db.session.delete(user_info)
            db.session.commit()

            flash("User has been deleted")
            return redirect("/")
        else:
            flash("THAT IS NOT ALLOWED!")
            return redirect("/")

# ADD FEEDBACK
@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    """ adds feedback. """

    if "username" not in session:
        flash("You must login first!")
        return redirect("/")
    else:
        user_info = User.query.get_or_404(username)

        form = FeedbackForm()

        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data

            new_feedback = Feedback(
                title=title, content=content, giver_name=session["username"], receiver_name=user_info.username)
            db.session.add(new_feedback)
            db.session.commit()

            return redirect(f"/users/{user_info.username}")
        else:
            return render_template("feedback.html", form=form)

# UPDATE FEEDBACK
@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Form to update existing feedback."""

    feedback_info = Feedback.query.filter_by(id=feedback_id).first()

    form = FeedbackForm(obj=feedback_info)

    if "username" not in session:
        flash("You must login first!")
        return redirect("/")
    elif session["username"] == feedback_info.giver_name and form.validate_on_submit():
        feedback_info.title = form.title.data
        feedback_info.content = form.content.data
        db.session.commit()

        return redirect(f"/users/{feedback_info.receiver_name}")
    else:
        return render_template("edit-feedback.html",
                               form=form,
                               feedback_info=feedback_info)

# DELETE FEEDBACK
@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete a particular feedback."""
    feedback_info = Feedback.query.filter_by(id=feedback_id).first()

    if session["username"] == feedback_info.giver_name:
        db.session.delete(feedback_info)
        db.session.commit()

        return redirect(f"/users/{feedback_info.receiver_name}")
