#!/usr/bin/env bash

set -e

if [ -z $1 ]; then
    echo "Declare which version part will be bumped"
    exit
fi

RELEASE_DIR=$(mktemp -d -t classifier-XXXXXXXXXX)
TOOLS_VIRTUALENV=$RELEASE_DIR/virtualenv_tools
CLASSIFIER_VIRTUALENV=$RELEASE_DIR/virtualenv_classifier
REPOSITORY=git@github.com:topicaxis/classifier.git

cd $RELEASE_DIR

virtualenv --python=python3 $TOOLS_VIRTUALENV
$TOOLS_VIRTUALENV/bin/pip install bumpversion flake8

virtualenv --python=python3 $CLASSIFIER_VIRTUALENV

git clone $REPOSITORY
cd classifier
git fetch --all

git checkout master
git merge develop

$TOOLS_VIRTUALENV/bin/bumpversion --commit --message "Released version {new_version}" --tag --tag-name "v{new_version}" $1

$TOOLS_VIRTUALENV/bin/flake8 classifier
$TOOLS_VIRTUALENV/bin/flake8 tests

$CLASSIFIER_VIRTUALENV/bin/python setup.py install
$CLASSIFIER_VIRTUALENV/bin/python setup.py test

git push origin master --tags

git checkout develop
git merge master
git push origin develop
