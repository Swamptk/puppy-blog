from flask import jsonify, request, make_response
from flask_restful import Resource
from project.models import User, BlogPost
from project.users.picture_handler import picture_from_url
from project import db
from datetime import datetime


# The `UserPostsApi` class is a Flask resource that retrieves all blog posts associated with a given
# username.
class UserPostsApi(Resource):
    def get(self, username:str):
        """
        The function retrieves all blog posts associated with a given username and returns them as a
        JSON response.
        
        :param username: The `username` parameter is a string that represents the username of a user
        :return: The code is returning a response containing JSON data. If the user has no posts, the
        response will include the message "user has no posts yet". If the user has posts, the response
        will include a list of JSON objects representing each post.
        """
        user: User = User.query.filter_by(username=username).one_or_404()
        posts: list[BlogPost] = BlogPost.query.filter_by(user_id=user.id).all()
        if len(posts) == 0:
            return make_response(jsonify({"info": "user has no posts yet"}))
        return make_response(jsonify([post.json() for post in posts]))


# The `ManageUsersApi` class provides methods to retrieve and delete user information from a database.
class ManageUsersApi(Resource):
    def get(self, username: str):
        """
        The function retrieves a user with a specific username and returns their information in JSON
        format.
        
        :param username: The `username` parameter is the username of the user we want to retrieve from
        the database
        :return: a response object that contains the JSON representation of the user object.
        """
        user: User = User.query.filter_by(username=username).one_or_404()
        return make_response(jsonify(user.json()))

    # TODO: only available with jwt_auth
    def delete(self, username: str):
        """
        The `delete` function deletes a user from the database based on their username and returns a
        success message.
        
        :param username: The `username` parameter is a string that represents the username of the user
        you want to delete from the database
        :return: a response object with a JSON payload indicating that the deletion was successful. The
        JSON payload includes a "success" key with the value "Deleted successfully."
        """
        user: User = User.query.filter_by(username=username).one_or_404()
        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify(success = "Deleted successfully."))


# The CreateUserApi class is a resource for creating user accounts.
class CreateUserApi(Resource):
    def post(self):
        """
        The above function is a POST request handler that creates a new user with the provided data and
        returns a response.

        :return: a response object with JSON data. The JSON data includes a success message and the
        user's information in JSON format. The response status code is 200.
        """
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
    
# The CreatePostApi class is a resource for creating posts.
class CreatePostApi(Resource):
    # TODO: only available with jwt_auth
    def post(self):
        """
        The above function is a POST request handler that creates a new blog post with the provided
        data.
        
        :return: The code is returning a response with JSON data. If the request does not contain any
        JSON data, a response with an error message "no data provided." is returned with a status code
        of 404. If the request contains the required fields (user_id, title, and text), a new BlogPost
        object is created and added to the database. If the optional field created_at is provided and in
        the given format, it sets it as the data of creation of the post.
        """
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