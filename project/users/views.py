"""
Views needed:
- Register
- Login
- Logout
- Account
- Update
- User's Blogpost
"""

from flask import (
    flash,
    render_template,
    redirect,
    Blueprint,
    request,
    url_for,
)
from flask_login import login_user, current_user, logout_user, login_required
from project import app, db
from flask_wtf.file import FileStorage
from project.models import User, BlogPost
from project.users.forms import LoginForm, RegistrationForm, UpdateForm
from project.users.picture_handler import add_profile_pic

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    """
    The `register` function handles the registration process for new users, including form validation
    and database insertion.
    :return: the rendered template "register.html" along with the form object.
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data,
        )
        with app.app_context():
            db.session.add(user)
            db.session.commit()
        flash("Thanks for your registration!", "success")
        return redirect(url_for("users.login"))
    return render_template("register.html", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    """
    The function `login()` handles the login process by validating the login form, checking if the user
    exists and the password is correct, and then logging in the user if the credentials are valid.
    :return: a rendered template for the login page, with the login form passed as a parameter.
    """
    form = LoginForm()
    if form.validate_on_submit():
        with app.app_context():
            user = User.query.filter_by(email=form.email.data).first()
        if not user:
            form.password.data = ""
            form.email.data = ""
            flash("The email is not registered.", "warning")
            return render_template("login.html", form=form)
        if user.check_password(form.password.data):
            login_user(user)
            flash(f"Loged in as {user.username}.", "success")
            next = request.args.get("next")
            if next == None or not next[0] == "/":
                next = url_for("core.index")
            return redirect(next)
        else:
            flash("Invalid password.", "danger")
            return render_template("login.html", form=form)
    return render_template("login.html", form=form)


@users.route("/acount")
@login_required
def account():
    """
    The function `account()` renders the account.html template with the current user's information and
    profile image.
    :return: the rendered template "account.html" with the variables "user" and "profile_img".
    """
    user: User = current_user # type: ignore
    profile_img = url_for("static", filename="profile_imgs/" + user.profile_img)
    return render_template("account.html", user=user, profile_img=profile_img)


@users.route("/update", methods=["GET", "POST"])
@login_required
def update():
    """
    The `update()` function handles the updating of user account information, including the profile
    picture, username, and email.
    :return: a response object that redirects the user to a specific route. The route depends on the
    outcome of the form validation and updates. If the form is not valid or there are no updates to be
    made, the user is redirected to the "users.update" route. If the form is valid and updates are made,
    the user is redirected to the "users.account" route.
    """
    form = UpdateForm()
    if form.validate_on_submit():
        if not form.any_updates(user=current_user): # type: ignore
            flash("Nothing to update.", "warning")
            return redirect(url_for("users.update"))
        updated = []
        with app.app_context():
            user = User.query.filter_by(email=current_user.email).first() # type: ignore
            if form.picture.data:
                pic: FileStorage = add_profile_pic(form.picture.data, user.username) # type: ignore
                user.profile_img = pic # type: ignore
                updated.append("profile picture")
            if form.username.data and form.username.data != user.username: # type: ignore
                user.username = form.username.data # type: ignore
                updated.append("username")
            if form.email.data and form.email.data != user.email: # type: ignore
                user.email = form.email.data # type: ignore
                updated.append("email")
            app.logger.info("Commiting changes")
            db.session.commit()
        flash(f"Account updated succesfully. Updated {', '.join(updated)}.", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username # type: ignore
        form.email.data = current_user.email # type: ignore
    return render_template("update.html", form=form)


@users.route("/<username>")
# @login_required
def posts(username: str):
    """
    The `posts` function retrieves and paginates blog posts written by a specific user and renders them
    on a template.
    
    :param username: The `username` parameter is the username of the user whose posts you want to
    retrieve
    :return: a rendered template called "user_posts.html" with the variables "posts" and "user" passed
    to it.
    """
    page = request.args.get("page", 1, int)
    with app.app_context():
        user = User.query.filter_by(username=username).first_or_404()
        posts = (
            BlogPost.query.filter_by(author=user)
            .order_by(BlogPost.created_at.desc())
            .paginate(page=page, per_page=5)
        )
        print(posts.first, posts.has_next, posts.has_prev, flush=True)
        return render_template("user_posts.html", posts=posts, user=user)


@users.route("/logout")
@login_required
def logout():
    """
    The `logout` function logs out the current user, flashes a message indicating the user has been
    logged out, and redirects them to the index page.
    :return: a redirect to the "core.index" route.
    """
    flash(f"You have been logged out from {current_user.username}.", "info") # type: ignore
    logout_user()
    return redirect(url_for("core.index"))
