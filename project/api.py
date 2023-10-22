from flask import jsonify, request, make_response
from flask_restful import Resource
from project.models import User, BlogPost
from project.users.picture_handler import picture_from_url
from project import db
from datetime import datetime


class UserPostsApi(Resource):
    def get(self, username):
        user: User = User.query.filter_by(username=username).one_or_404()
        posts: list[BlogPost] = BlogPost.query.filter_by(user_id=user.id).all()
        if len(posts) == 0:
            return make_response(jsonify({"info": "user has no posts yet"}))
        return make_response(jsonify([post.json() for post in posts]))


class ManageUsersApi(Resource):
    def get(self, username):
        user: User = User.query.filter_by(username=username).one_or_404()
        return make_response(jsonify(user.json()))

    # TODO: only available with jwt_auth
    def delete(self, username):
        user: User = User.query.filter_by(username=username).one_or_404()
        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify(success = "Deleted successfully."))


class CreateUserApi(Resource):
    def post(self):
        json: dict | None = request.json
        if not json:
            resp_data = jsonify(error = "no data provided.")
            return make_response(resp_data,404)
        username = json.get("username")
        email = json.get("email")
        password = json.get("password")
        picture_url = json.get("picture_url")
        created_at = json.get("created_at")

        if username and email and password:
            user = User(email, username, password)
        else:
            resp_data = jsonify(error= "must provide username, email and password")
            return make_response(resp_data,404)

        if picture_url:
            profile_pic = picture_from_url(picture_url, username)
            user.profile_img = profile_pic

        if created_at:
            try:
                date = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
                user.created_at = date
            except ValueError:
                resp_data = jsonify(error = "date format was not valid.",format = "%Y-%m-%d %H:%M:%S")
                return make_response(resp_data, 404)
        db.session.add(user)
        db.session.commit()
        resp_data = jsonify({"success": "user created successfully", "user": user.json()})
        return make_response(resp_data, 200)

class CreatePostApi(Resource):
    # TODO: only available with jwt_auth
    def post(self):
        json = request.json
        if not json: 
            resp_data = jsonify(error = "no data provided.")
            return make_response(resp_data, 404)
        user_id = json.get("user_id")
        title = json.get("title")
        text = json.get("text")
        created_at = json.get("created_at")
        if user_id and title and text:
            post = BlogPost(user_id, title, text) 
        else:
            resp_data = jsonify(error = "must provide user_id, title and text")
            return make_response(resp_data, 404)
        if created_at:
            try:
                date = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
                post.created_at = date
            except ValueError:
                resp_data = jsonify({"error": "date format was not valid.","format": "%Y-%m-%d %H:%M:%S"})
                return make_response(resp_data, 404)
        db.session.add(post)
        db.session.commit()
        resp_data = jsonify({"success": "post created successfully", "post": post.json()})
        return make_response(resp_data, 200)