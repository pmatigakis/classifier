import requests


def main():
    classifier_url = "http://192.168.1.103:8022"
    data = [8.0, 1.0, 7.0, 0.0, 15.0, 7.0, 6.0, 5.0, 3.0, 1.0]

    response = requests.post("{}/api/v1/predict/multilabel".format(classifier_url), json={"data": [data]})
    print(response.json())

    response = requests.post("{}/api/v1/predict/multilabel-probabilities".format(classifier_url), json={"data": [data]})
    print(response.json())


if __name__ == "__main__":
    main()
