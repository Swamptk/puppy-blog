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
from project.models import User, BlogPost
from project.users.forms import LoginForm, RegistrationForm, UpdateForm
from project.users.picture_handler import add_profile_pic

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
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
    user: User = current_user # type: ignore
    profile_img = url_for("static", filename="profile_imgs/" + user.profile_img)
    return render_template("account.html", user=user, profile_img=profile_img)


@users.route("/update", methods=["GET", "POST"])
@login_required
def update():
    form = UpdateForm()
    if form.validate_on_submit():
        if not form.any_updates(user=current_user): # type: ignore
            flash("Nothing to update.", "warning")
            return redirect(url_for("users.update"))
        updated = []
        with app.app_context():
            user = User.query.filter_by(email=current_user.email).first() # type: ignore
            if form.picture.data:
                pic = add_profile_pic(form.picture.data, user.username) # type: ignore
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
def posts(username):
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
    flash(f"You have been loged out from {current_user.username}.", "danger") # type: ignore
    logout_user()
    return redirect(url_for("core.index"))
