"""
This module contains functions to download json data from the web
"""
import requests


def get_json(url):
    """
    get_json(url)
    url: url of the json data to download
    returns: json data dictionary
    """
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        data = response.json()
        return data

    return False


# print(get_json("https://jsonplaceholder.typicode.com/todos/1"))
