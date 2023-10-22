import os
import requests
from PIL import Image
from flask import url_for, current_app
from io import BytesIO
from flask_wtf.file import FileStorage


def add_profile_pic(pic_upload: FileStorage, username: str):
    '''The function `add_profile_pic` takes a file upload and a username as input, renames the file to
    match the username, resizes the image to a specified size, and saves it to a specified filepath.
    
    Parameters
    ----------
    pic_upload : FileStorage
        The `pic_upload` parameter is of type `FileStorage` and represents the uploaded profile picture
    file.
    username : str
        The `username` parameter is a string that represents the username of the user for whom the profile
    picture is being uploaded.
    
    Returns
    -------
        the filename of the stored profile picture.
    
    '''
    # blablabla.jpg --> username.jpg
    filename: str = pic_upload.filename # type: ignore
    ext_type = filename.split(".")[-1]
    storage_filename = str(username) + "." + ext_type
    filepath = os.path.join(
        current_app.root_path, "static", "profile_imgs", storage_filename
    )
    output_size = (200, 200)
    pic = Image.open(pic_upload) # type: ignore
    pic.thumbnail(output_size)
    pic.save(filepath)
    return storage_filename


def picture_from_url(url: str, username: str):
    '''The function `picture_from_url` downloads an image from a given URL, resizes it to 200x200 pixels,
    and saves it to a specified filepath with a filename based on the given username.
    
    Parameters
    ----------
    url : str
        The `url` parameter is a string that represents the URL of the image you want to download and save.
    username : str
        The `username` parameter is a string that represents the username of the user for whom the profile
    picture is being saved.
    
    Returns
    -------
        the filename of the saved picture.
    
    '''
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
