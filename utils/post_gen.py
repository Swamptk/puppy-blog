from random import choice
from project import app
import json
from project.models import User
import requests


def create_post(base_url: str, user_id: int, post: dict[str, str]):
    api_url = "/api/createpost"
    url = base_url + api_url
    post["user_id"] = user_id  # type: ignore
    response = requests.post(url, json=post)
    return response


def create_posts(base_url:str, posts_file: str):
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

