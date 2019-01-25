"""
Python script for login and logout the NJU network account
"""


from urllib import parse, request

import argparse
import json


__all__ = [
    "login",
    "logout",
    "ShowResponse",
]


_URLs = {
    "login": "http://p.nju.edu.cn/portal_io/login",
    "logout": "http://p.nju.edu.cn/portal_io/logout",
}


def login(username, password):
    """
    Logging in to the NJU network account

    Parameters
    ----------
    username : str
    password : str

    Returns
    -------
    response : dict
        The response from the server
    """

    if not isinstance(username, str) or not isinstance(password, str):
        raise ValueError(
            "The `username` and `password` parameter must be string"
        )

    params = parse.urlencode({
        'username': username,
        "password": password,
    }).encode("ascii")

    with request.urlopen(_URLs["login"], data=params) as fp:
        response = json.loads(fp.read().decode("utf-8"))
    return response


def logout():
    """
    Logging out from the NJU network account

    Returns
    -------
    response : dict
        The response from the server
    """

    with request.urlopen(_URLs["logout"]) as fp:
        response = json.loads(fp.read().decode("utf-8"))
    return response


def ShowResponse(response, *, verbose=False):
    """
    Show the response from the server

    Parameters
    ----------
    response : dict
        The content of the response
    verbose : boolean, optional
        Whether to display the full content of the response
        default: False
    """

    if verbose:
        for key, value in response.items():
            if isinstance(value, dict):
                print(f"{key}: " + "{")
                for sub_key, sub_value in value.items():
                    print(f"    {sub_key}: {sub_value}")
                print("}")
            else:
                print(f"{key}: {value}")
    else:
        print(f"reply_msg: {response['reply_msg']}")


def ArgParser():
    """
    Parsing the command line arguments
    """

    parser = argparse.ArgumentParser(
        description="Login or logout the NJU network account!"
    )
    parser.add_argument(
        "action", type=str, choices=("login", "logout"),
        help="Login or logout the NJU network account?"
    )

    parser.add_argument("-u", "--username", type=str, help="The username.")
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Show the full content of the response from the server."
    )

    args = parser.parse_args()
    return args.action, args.username, args.verbose


if __name__ == "__main__":
    from getpass import getpass

    action, username, verbose = ArgParser()
    if action == "login":
        if username is None:
            username = input("Username:")
        response = login(username=username, password=getpass())
    else:
        response = logout()
    ShowResponse(response, verbose=verbose)