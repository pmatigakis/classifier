import requests


def main():
    username = "username"
    password = "password"

    credentials = {
        "username": username,
        "password": password
    }

    response = requests.post("http://localhost:5000/auth", json=credentials)

    token = response.json()["access_token"]

    data = [5.6, 2.8, 4.9, 2.0]

    headers = {
        "Authorization": "JWT %s" % token
    }

    response = requests.post("http://localhost:5000/api/classify", headers=headers, json={"data": data})

    print response.json()

if __name__ == "__main__":
    main()
