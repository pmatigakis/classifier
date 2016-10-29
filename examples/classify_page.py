from argparse import ArgumentParser

import requests

from classifier.helpers import process_web_page


def get_arguments():
    parser = ArgumentParser()

    parser.add_argument("--username")
    parser.add_argument("--password")
    parser.add_argument("--url")

    return parser.parse_args()


def get_access_token(username, password):
    credentials = {
        "username": username,
        "password": password
    }

    response = requests.post("http://localhost:5000/auth", json=credentials)

    return response.json()["access_token"]


def get_page_contents(url, access_token):
    headers = {
        "Authorization": "JWT %s" % access_token,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36"
    }

    response = requests.get(url, headers=headers, verify=False)

    contents = process_web_page(response.text)

    return contents


def classify_text(text, access_token):
    headers = {
        "Authorization": "JWT %s" % access_token,
    }

    params = {
        "content": text
    }

    response = requests.post("http://localhost:5000/api/v1/query", json=params, headers=headers)

    return response.json()


def main():
    args = get_arguments()

    access_token = get_access_token(args.username, args.password)

    contents = get_page_contents(args.url, access_token)

    result = classify_text(contents, access_token)

    print result


if __name__ == "__main__":
    main()
