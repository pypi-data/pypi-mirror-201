"""Call Jokes API & Parse it to simple text"""

import json
from urllib import request

URL = "https://v2.jokeapi.dev/joke/Any?safe-mode" # Safe jokes by default


def get_joke(single_joke: bool = True) -> dict:
    """fetches jokes from v2.jokeapi.dev, uses Python std library.

    Args:
        single_joke (bool, optional): Flag to fetch single or two part jokes. Defaults to True.

    Returns:
        dict: JSON response dict from joke api
    """
    if single_joke:
        response = request.urlopen(f"{URL}&type=single")
    else:
        response = request.urlopen(f"{URL}&type=twopart")
    return json.loads(response.read())


def parse_joke(joke: dict) -> str:
    """parse jokes received from Jokes API

    Args:
        joke (dict): JSON response in Python dict

    Returns:
        str: Joke formatted as Python string
    """
    joke_type = joke.get("type")
    if joke_type == "single":
        joke = joke.get("joke")
    elif joke_type == "twopart":
        one = joke.get("setup")
        two = joke.get("delivery")
        joke = f"Q) {one}\nA){two}"
    else:
        joke = "Funny story - the API failed!"
    return joke


def main():
    """Calls all functions under this function"""
    joke = get_joke()
    print(parse_joke(joke))


if __name__ == "__main__":
    main()
