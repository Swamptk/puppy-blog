"""
For BlogPosts
- Create
- View
- Edit
- Delete
"""

from flask import abort, flash, redirect, render_template, Blueprint, request, url_for
from flask_login import current_user, login_required
from project import db, app
from project.models import BlogPost
from project.posts.forms import BlogPostForm

blog_posts = Blueprint("blog_posts", __name__)


@blog_posts.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = BlogPostForm()
    if form.validate_on_submit():
        blog_post = BlogPost(
            title=form.title.data, text=form.text.data, user_id=current_user.id
        )
        with app.app_context():
            db.session.add(blog_post)
            db.session.commit()
        flash("Blog Post Created!", "success")
        return redirect(url_for("core.index"))
    return render_template("create_post.html", form=form)


@blog_posts.route("/posts/<int:blog_post_id>")
def view(blog_post_id):
    with app.app_context():
        blog_post = BlogPost.query.get_or_404(blog_post_id, "Post not found.")
        author = blog_post.author
    return render_template("view_post.html", post=blog_post, author=author)


@blog_posts.route("/posts/<int:blog_post_id>/update", methods=["GET", "POST"])
@login_required
def update(blog_post_id):
    with app.app_context():
        blog_post: BlogPost = BlogPost.query.get_or_404(blog_post_id, "Post not found.")
        author = blog_post.author
        if author.id != current_user.id:
            flash("Only the author can edit the post.", "danger")
            abort(403)
        form = BlogPostForm()
        if form.validate_on_submit():
            blog_post.title = form.title.data
            blog_post.text = form.text.data
            db.session.commit()
            flash("Blog post updated successfully.", "success")
            return redirect(url_for("blog_posts.view", blog_post_id=blog_post_id))
        elif request.method == "GET":
            form.title.data = blog_post.title
            form.text.data = blog_post.text
    return render_template("create_post.html", form=form)


@blog_posts.route("/posts/<int:blog_post_id>/delete", methods=["GET", "POST"])
@login_required
def delete(blog_post_id):
    with app.app_context():
        blog_post: BlogPost = BlogPost.query.get_or_404(blog_post_id, "Post not found.")
        author = blog_post.author
        if author.id != current_user.id:
            flash("Only the author can delete the post.", "danger")
            abort(403)
        db.session.delete(blog_post)
        db.session.commit()
        flash("Post deleted successfully.", "success")
    return redirect(url_for("core.index"))
