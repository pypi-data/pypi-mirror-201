"""
This module contains functions to download images from the web
"""
import shutil

import requests


def get_image(url, filename):
    # document this function with a docstring
    """
    get_image(url, filename)
    url: url of the image to download
    filename: name of the file to save the image to
    returns: Boolean
    """
    response = requests.get(url, stream=True, timeout=5)
    if response.status_code == 200:
        response.raw.decode_content = True
        # context managers Corey Schafer
        with open(filename, "wb") as file:
            shutil.copyfileobj(response.raw, file)
            print("Image successfully Downloaded: ", filename)
        return True

    print("Image couldn't be retrieved")
    return False


# get_image(
#     "https://th.bing.com/th/id/R.fcd349af80cb44e5a32bc3696019cf5f?rik=8bH1xMwmkghXvg&pid=ImgRaw&r=0",
#     "test.jpg",
# )
