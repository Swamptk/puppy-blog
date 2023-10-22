from time import sleep
import requests


def get_users_json(api_url: str) -> list[dict[str, str | dict[str, str]]]:
    """
    The function `get_users_json` retrieves user data from an API and returns it as a list of
    dictionaries.

    :param api_url: The `api_url` parameter is a string that represents the URL of the API endpoint from
    which we want to retrieve user data
    :return: a list of dictionaries, where each dictionary represents a user. The keys in the dictionary
    are strings, and the values can be either strings or nested dictionaries.
    """
    response = requests.get(api_url)
    results: list[dict] = response.json()["results"]
    return results


def parse_user_json(json: dict) -> dict[str, str | None]:
    """
    The function `parse_user_json` takes a JSON object as input and extracts specific data fields such
    as email, username, password, created_at, and picture_url from it.

    :param json: The `json` parameter is a dictionary that represents a user's data in JSON format. It
    contains various fields such as email, login information, registration details, and picture URL. The
    function `parse_user_json` takes this JSON data and extracts specific fields to create a new
    dictionary `user_data`
    :return: The function `parse_user_json` returns a dictionary containing the parsed user data. The
    keys in the dictionary are "email", "username", "password", "created_at", and "picture_url". The
    values for these keys are obtained from the input JSON dictionary.
    """
    user_data = {}
    user_data["email"] = json.get("email")
    if login := json.get("login"):
        user_data["username"] = login.get("username")
        user_data["password"] = login.get("password")
    if registered := json.get("registered"):
        created_at = registered.get("date")
        user_data["created_at"] = "".join(
            c if not c.isalpha() else " " for c in created_at.split(".")[0]
        )
    if picture := json.get("picture"):
        user_data["picture_url"] = picture.get("large")
    return {
        "email": user_data.get("email"),
        "username": user_data.get("username"),
        "password": user_data.get("password"),
        "created_at": user_data.get("created_at"),
        #! randomuser api fails if request images too fast.
        "picture_url": user_data.get("picture_url"),
    }


def generate_user(user: dict[str, str | None], base_url: str) -> requests.Response:
    """
    The function generates a user by sending a POST request to a specified URL with user data in JSON
    format.

    :param user: A dictionary containing the user information to be sent in the request body
    :param base_url: The `base_url` parameter is a string that represents the base URL of the API endpoint where
    the user will be created. It should include the protocol (e.g., "http://" or "https://") and the
    domain name (e.g., "example.com")
    :return: the response from the POST request made to the specified URL with the user data as JSON.
    """
    base_url = base_url + "/api/createuser"
    response = requests.post(base_url, json=user)
    return response

def create_users(base_url: str, n_users: int):
    """
    The `create_users` function generates random users using the RandomUser API, parses the user data,
    generates a user using the `generate_user` function, and saves the user information to a file.
    
    :param base_url: The `base_url` parameter is the base URL of the API or website where you want to
    create the users. It is the URL that will be used as the endpoint to send the user creation requests
    :param n_users: The `n_users` parameter is the number of random users you want to create. It
    determines how many API calls will be made to the randomuser API to generate the users
    """
    api_url = f"https://randomuser.me/api/?results={n_users}"
    results = get_users_json(api_url)
    for result in results:
        user = parse_user_json(result)
        response = generate_user(user, base_url)
        with open("generated_users.txt", "a") as f:
            f.write(f"{user['email']} | {user['password']} | {user['picture_url']}\n")
        print(response)
        #! Needed so the randomuser api doesn't block the conection
        sleep(1)

if __name__ == "__main__":
    base_url = "http://127.0.0.1:5000"
    create_users(base_url, 5)