FROM python:3.5.2

WORKDIR /app

COPY ./docker-entrypoint.sh /app
ADD classifier /app/classifier
COPY setup.py /app
COPY requirements.txt /app
COPY requirements-test.txt /app
COPY MANIFEST.in /app

# you will have to modify the settings file according to your needs before
# building the docker image
COPY configuration/settings.py /app/configuration/

# the example classifiers are added for testing. You will also want to change
# this and add your own classifiers somehow
ADD examples /app/examples

RUN pip install .

# this has to be the same as the port that is defined in the settings
EXPOSE 8022

ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["run"]
