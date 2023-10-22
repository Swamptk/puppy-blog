from flask import jsonify, request
from flask_restful import Resource
from project.models import User, BlogPost
from project.users.picture_handler import picture_from_url
from project import db
from datetime import datetime

class UserPostsApi(Resource):

    def get(self, username):
        user: User = User.query.filter_by(username=username).one_or_404()
        posts: list[BlogPost] = BlogPost.query.filter_by(user_id = user.id).all()
        if len(posts) == 0:
            return jsonify({"info":"user has no posts yet"})
        return jsonify([post.json() for post in posts])

class ManageUsers(Resource):
    def get(self,username):
        user = User.query.filter_by(username=username).one_or_404()
        

class CreateUserApi(Resource):
    def post(self):
        json: dict | None = request.json
        if not json:
            return jsonify({"error":"no data provided"}), 404
        username = json.get('username')
        email = json.get('email')
        password = json.get('password')
        picture_url = json.get('thumbnail')
        created_at = json.get('created_at')
        
        if username and email and password:
            user = User(email,username,password)
        else:
            return jsonify({"error": "must provide username, email and password"})

        if picture_url:
            profile_pic = picture_from_url(picture_url, username)
            user.profile_img = profile_pic

        if created_at:
            try:
                date = datetime.strptime(created_at,"%Y-%m-%d %H:%M:%S")
            except ValueError:
                return jsonify({"error":"date format was not valid.", "format": "%Y-%m-%d %H:%M:%S"})
            user.created_at = date
        
        db.session.add(user)
        db.session.commit()
        return jsonify("")
