## Things learnt in this project

### TimeStamped abstract model base

Here we use the `TimedBase` class as a base model that will add automatically the datetime when the entry was created for any model that inherits from it. Since it inherits from the normal `Base`, when calling `Base.metadata.create_all()` it will also create those models.

#### **`project.models.base.py`**
```python
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
# Normal Base class
class Base(DeclarativeBase):
    pass
# Base with defaul date_created
class TimedBase(Base):
    __abstract__ = True
    date_created: Mapped[datetime] = mapped_column(default=datetime.now())
```

### Handling Errors

The views file when we reffer to error pages is usually called `handlers.py` by convention.
#### **`project.error_pages.handlers.py`**
```python
from flask import Blueprint, render_template
# Only needed if working with templates
error_pages = Blueprint("error_pages", __name__)
# We use app_errorhandler instead of route
@error_pages.app_errorhandler(404)
def error_404(error):
    return render_template("error_pages/404.html"), 404
```

### Accepting files in a form 

We do this through the module `flask_wtf.file`
#### **`project.users.forms`**
```python
from flask_wtf.file import FileField, FileAllowed

picture = FileField("Profile Picture", validators=[FileAllowed(["jpg", "png"])])
```

Now, to handle Image files, we need to use a picture handler and the module `pillow`.
#### **`project.users.picture_handler.py`**
```python
from PIL import Image # pillow
from flask import url_for, current_app

def add_profile_pic(pic_upload, username):
    # Blablabla.jpg --> username.jpg
    filename = pic_upload.filename
    ext_type = filename.split(".")[-1]
    storage_filename = str(username) + "." + ext_type
    # Path where the picture will be stored
    filepath = os.path.join(
        current_app.root_path, "static", "profile_pics", storage_filename
    )
    # Open the image to treat it with pillow
    pic = Image.open(pic_upload)
    # Resize it 
    output_size = (200, 200)
    pic.thumbnail(output_size)
    # Save the edited image into the specified filepath
    pic.save(filepath)
    # Return username.jpg
    return storage_filename
```

Finally, in the form tag inside the html file we need to state:
```html
<form method="POST" action="" enctype="multipart/form-data">
```

### Flask-SQLAlchemy vs SQLAlchemy alone

It is way better to use Flask-SQLAlchemy. 

For the app configuration just do as before with `db = SQLAlchemy(app)`.
For queries use `app.app_context` and `db.session` or `Model.query`.
For the models just use `db.Model` as you used `Base` before.

Important to perform migrations too.

You can still use declarative stuff like `Mapped`, `mapped_column` and `relationship` as you did before.

### Pagination

In order to perform pagination easily we will need to work over a `flask_sqlalchemy.SQLAlchemy` model. This is because Flask will give us the opportunity to work with the method `.pagination()`.

To present several Blog Posts in different pages of the same route we would do as follows:

#### **`project.users.views.py`**
```python
@users.route("/<username>")
@login_required
def posts(username):
    # We get page as an arg from our request, with default 1 since we are not passing any
    # Later, through html we will pass this argument to the request
    page = request.args.get("page", 1, int)
    with app.app_context():
        # Get the user named in the url, if doesn't exist abort(404)
        user = User.query.filter_by(username=username).first_or_404()
        # Get all the posts from the user, order them by descending creation date
        posts = (
            BlogPost.query.filter_by(author=user)
            .order_by(BlogPost.created_at.desc())
            # show 5 posts per page and the current page is the arg we pass with the req
            .paginate(page=page, per_page=5)
        )
        # We pass the current page posts to the template
        return render_template("user_posts.html", posts=posts, user=user)
```

#### **`project.templates.user_posts.html`**
```html
<!-- We can iterate through the posts items to get each BlogPost instance -->
{% for post in posts.items %}
<h1 class="display-4">{{post.title}}</h1>
<p class="lead">By <a href="{{url_for('users.posts', username = post.author.username)}}">
    @{{ post.author.username }}
</a>
</p>
<p class="text-muted">Created at {{ post.created_at.strftime('%a %d %b %Y') }}.</p>
<p>{{ post.text }}</p>
{% endfor %}
<!-- We can use bootstrap to create a paginator to walk through the pages -->
<nav aria-label="Posts navigation">
    <ul class="pagination justify-content-center">
    <!-- If this is the first page, disable the 'previous' button -->
        {% if posts.has_prev %}
        <li class="page-item">
            {% else %}
        <li class="page-item disabled">
            {% endif %}
            <!-- Pay attention to the url_for -->
            <a class="page-link" href="{{url_for('users.posts', username=user.username, page=posts.page-1)}"
                aria-label="Previous">
                <span aria-hidden="true">&laquo;</span>
            </a>
        </li>
        <!-- .iter_pages() allow us to get the indices of the pages -->
        {% for page_num in posts.iter_pages(left_edge=1, right_edge=1, left_current=1, right_current=2) %}
        {% if posts.page == page_num %}
        <!-- Disable if the number is the current page -->
        <li class="page-item active disabled" aria-current="page">
            <a class="page-link" href="{{url_for('users.posts', username=user.username, page=page_num)}}">
                {{ page_num }}</a>
        </li>
        {% else %}
        <li class="page-item" aria-current="page">
            <a class="page-link" href="{{url_for('users.posts', username=user.username, page=page_num)}}">
                {{ page_num }}</a>
        </li>
        {% endif %}
        {% endfor %}
        {% if posts.has_next %}
        <li class="page-item">
            {% else %}
        <li class="page-item disabled">
            {% endif %}
            <a class="page-link" href="{{url_for('users.posts', username=user.username, page=posts.page+1)}"
                aria-label="Next">
                <span aria-hidden="true">&raquo;</span>
            </a>
        </li>
    </ul>
</nav>
```

### Check if the User is Logged in

We can do this with the decorator `@loggin_required` from `flask_login` or inside the html file using if statements:
```html
{% if current_user.is_authenticated %}
<h1>You are logged in!</h1>
{% else %}
<h1>You are not logged in!</h1>
{% endif %}
```