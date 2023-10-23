# Puppy Blog Project 🐶
Puppy and pet related blog web app using Flask.

## Description
Blog web application created using `Flask` and `Jinja` templates, . The web supports user management and blog post management using both the web page and the API.

The data is stored using `SQLite` and the db is managed using `SQLAlchemy` and `SQLAlchemy`. We use `Flask_login` and `Werkzeug` for the login and password hashing process. The site also provides an API using `Flask_Restful`. To randomly generate users for demonstration we have used the [random user generator open-source API](https://randomuser.me/) and [ChatGPT](https://chat.openai.com/) for the demonstration blog posts.

# Installation

For the installation, it is highly recommendable to create a python environment (for example using [Conda](https://www.anaconda.com/)). The project uses `Python=3.11.5`.

Use the package manager [pip](https://pypi.org/project/pip/) to install the packages stated in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

After the installation is done, just run the app using python to check that everything has been installed correctly:

```bash
python app.py
```