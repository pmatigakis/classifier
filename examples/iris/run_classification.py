import requests


def main():
    data = [5.6, 2.8, 4.9, 2.0]

    response = requests.post("http://localhost:5000/api/v1/predict/iris", json={"data": data})

    print response.json()

if __name__ == "__main__":
    main()
