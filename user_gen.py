from datetime import datetime
import requests
from io import BytesIO


n_users = 5
api_url = f"https://randomuser.me/api/?results={n_users}"


def get_users_json(api_url: str):
    response = requests.get(api_url)
    results: list[dict] = response.json()["results"]
    return results


def parse_user_json(json: dict):
    user_data = {}
    user_data["email"] = json.get("email")
    if login := json.get("login"):
        user_data["username"] = login.get("username")
        user_data["password"] = login.get("password")
    if registered := json.get("registered"):
        created_at = registered.get("date")
        user_data["created_at"] = "".join(c if not c.isalpha() else " " for c in created_at.split(".")[0] )
    if picture := json.get("picture"):
        user_data["picture_url"] = picture.get("large")

    return {
        "email": user_data.get("email"),
        "username": user_data.get("username"),
        "password": user_data.get("password"),
        "created_at": user_data.get("created_at"),
        # "picture_url": user_data.get("picture_url"),
    }

def generate_user(user: dict, url: str):
    url = url + "/api/createuser"
    response = requests.post(url, json=user)
    return response

if __name__ == "__main__":
    url = "http://127.0.0.1:5000"
    results = get_users_json(api_url)
    for result in results:
        user = parse_user_json(result)
        response = generate_user(user, url)
        with open("generated_users.txt", "a") as f:
            f.write(f"{user['email']}, {user['password']} \n")
        print(response)
    
