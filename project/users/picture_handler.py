import os
import requests
from PIL import Image
from flask import url_for, current_app
from io import BytesIO


def add_profile_pic(pic_upload, username):
    # Blablabla.jpg --> username.jpg
    filename = pic_upload.filename
    ext_type = filename.split(".")[-1]
    storage_filename = str(username) + "." + ext_type
    filepath = os.path.join(
        current_app.root_path, "static", "profile_imgs", storage_filename
    )
    output_size = (200, 200)
    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)
    return storage_filename


def picture_from_url(url: str, username: str):
    ext_type = url.split(".")[-1]
    storage_filename = str(username) + "." + ext_type
    filepath = os.path.join(
        current_app.root_path, "static", "profile_imgs", storage_filename
    )
    response = requests.get(url)
    output_size = (200, 200)
    pic = Image.open(BytesIO(response.content))
    pic.thumbnail(output_size)
    pic.save(filepath)
    return storage_filename
