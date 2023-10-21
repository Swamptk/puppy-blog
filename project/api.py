from flask import jsonify
from flask_restful import Resource
from project.models import User, BlogPost

class UserPostsApi(Resource):

    def get(self, username):
        user: User = User.query.filter_by(username=username).one_or_404()
        posts: list[BlogPost] = BlogPost.query.filter_by(user_id = user.id).all()
        if len(posts) == 0:
            return jsonify({"info":"user has no posts yet"})
        return jsonify([post.json() for post in posts])


        

