import os
from sqlalchemy.orm import declarative_base
from flask_restful import Api
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

##### Dirs
base_path = os.path.abspath(os.path.dirname(__file__))
db_path = "sqlite:///" + os.path.join(base_path, "database.db")

##### Base Model
Base = declarative_base()
db = SQLAlchemy(model_class=Base)

##### App
app = Flask(__name__)
#! Change this
app.config['SECRET_KEY'] = "mysecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.__init__(app)
Migrate(app,db)

##### Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login" # type: ignore

##### BluePrints
from project.core.views import core
from project.users.views import users
from project.posts.views import blog_posts
from project.error_pages.handlers import error_pages

app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(blog_posts)
app.register_blueprint(error_pages)

##### API
from project.api import UserPostsApi,CreateUserApi, ManageUsersApi, CreatePostApi
api = Api(app)
api.add_resource(UserPostsApi, "/api/getuserposts/<username>")
api.add_resource(CreateUserApi, "/api/createuser")
api.add_resource(ManageUsersApi, "/api/<username>")
api.add_resource(CreatePostApi, "/api/createpost")

##### Create DB
with app.app_context():
    db.create_all()

app.logger.info("App started successfully")