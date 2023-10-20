from project import app
from flask import render_template, request, Blueprint
from project.models import BlogPost

core = Blueprint("core", __name__)


@core.route("/")
def index():
    page = request.args.get("page", 1, int)
    with app.app_context():
        posts = BlogPost.query.order_by(BlogPost.created_at.desc()).paginate(
            page=page, per_page=5
        )
        # posts.iter_pages()
        return render_template("index.html", posts=posts)


@core.route("/info")
def info():
    return render_template("info.html")
