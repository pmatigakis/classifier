import requests

import settings

def main():
    data = [5.6, 2.8, 4.9, 2.0]

    response = requests.post("http://{}:{}/api/v1/predict/iris".format(settings.HOST, settings.PORT), json={"data": data})

    print response.json()

if __name__ == "__main__":
    main()
