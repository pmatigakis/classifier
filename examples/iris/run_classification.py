import requests


def main():
    classifier_url = "http://192.168.1.103:8022"
    data = [5.6, 2.8, 4.9, 2.0]

    response = requests.post("{}/api/v1/predict/iris".format(classifier_url), json={"data": [data]})
    print(response.json())

    response = requests.post("{}/api/v1/predict/iris-probabilities".format(classifier_url), json={"data": [data]})
    print(response.json())


if __name__ == "__main__":
    main()
