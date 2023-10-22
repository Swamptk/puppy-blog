from random import choice
from project import app
import json
from project.models import User
import requests


def create_post(base_url: str, user_id: int, post: dict[str, str]):
    """
    The function `create_post` sends a POST request to a specified API endpoint with a user ID and a
    post dictionary as JSON data.
    
    :param base_url: The `base_url` parameter is a string that represents the base URL of the API
    endpoint you want to send the POST request to. It should include the protocol (e.g., "http://" or
    "https://") and the domain name or IP address
    :param user_id: The `user_id` parameter is an integer that represents the ID of the user who is
    creating the post
    :param post: The `post` parameter is a dictionary that contains the details of the post. It should
    have the following keys:
    :return: the response object from the POST request.
    """
    api_url = "/api/createpost"
    url = base_url + api_url
    post["user_id"] = user_id  # type: ignore
    response = requests.post(url, json=post)
    return response


def create_posts(base_url:str, posts_file: str):
    """
    The function `create_posts` creates posts by randomly selecting a user ID from a list of user IDs
    and then calling the `create_post` function with the selected user ID and the post data.
    
    :param base_url: The base URL is the base address of the API endpoint where you want to create the
    posts. It should include the protocol (e.g., "http://") and the domain name (e.g., "example.com")
    :param posts_file: The `posts_file` parameter is the file path to a JSON file that contains the
    posts data. This file should have a key called "posts" which contains a list of post objects
    :return: The function does not explicitly return anything.
    """
    with app.app_context():
        users = User.query.all()
        if len(users) == 0:
            print("No users in the db. Create some first.")
            return 
        ids = [u.id for u in users]

    with open(posts_file, "r") as f:
        posts = json.load(f)["posts"]

    for post in posts:
        user_id = choice(ids)
        response = create_post(base_url,user_id,post)
        print(response)

