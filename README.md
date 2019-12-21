[![Build Status](https://travis-ci.org/pmatigakis/classifier.svg?branch=develop)](https://travis-ci.org/topicaxis/classifier)
[![codecov](https://codecov.io/gh/pmatigakis/classifier/branch/develop/graph/badge.svg)](https://codecov.io/gh/topicaxis/classifier)

A Flask web application that exposes a scikit-learn classifier over an REST API endpoint

This application is used by TopicAxis API to classify the contents of a web page.
The scikit-learn model that is used can be found at the [trained-models](https://github.com/topicaxis/trained-models)
repository. See the documentation for instructions on how to use this model.

# Installation

Download the source code and install the latest stable version using pip.

```bash
git clone https://github.com/pmatigakis/classifier.git
cd classifier
git fetch --all
git checkout master
pip install .
```

# Configuration

A `settings.py` file  is required in the folder where the classifier will be started.
See the example settings file in the `configuration` folder for information about
what configuration settings are available. Most of the configuration variables
in the example settings file can be modified using environment variables. Rename
`configuration/.env.template` to `configuration/.env` and change what is required.

# Running

Go into the folder with the settings file and start the server.

```bash
classifier-server
```

The classification endpoint is at `http://<HOST>:<PORT>/api/v1/predict/<CLASSIFIER>`.
To run a prediction execute a POST request to that endpoint. For example to run
a prediction using the demo Iris classifier execute the following request.

```bash
curl -X POST -H "Content-Type: application/json" -d '{"data": [[4.8,3.0,1.4,0.1]]}' http://192.168.1.103:8022/api/v1/predict/iris
```

The response status code should be `200` and the response should look like this

```json
{
    "results": ["Iris-setosa"]
}
```
