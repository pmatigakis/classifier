[![Build Status](https://travis-ci.org/topicaxis/classifier.svg?branch=develop)](https://travis-ci.org/topicaxis/classifier)
[![codecov](https://codecov.io/gh/topicaxis/classifier/branch/develop/graph/badge.svg)](https://codecov.io/gh/topicaxis/classifier)

A Flask web application that exposes a scikit-learn classifier over an REST API endpoint

For usage instructions use Sphinx to build the documentation in the `docs` folder.

This application is used by TopicAxis API to classify the contents of a web page.
The scikit-learn model that is used can be found at the [trained-models](https://github.com/topicaxis/trained-models)
repository. See the documentation for instructions on how to use this model.
