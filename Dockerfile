FROM python:2.7.14

WORKDIR /app

ADD classifier /app/classifier
COPY setup.py /app
COPY configuration/settings.py /app/configuration/

RUN pip install scipy==0.18.0 numpy==1.11.1
RUN pip install scikit-learn==0.17.1
RUN python setup.py install
RUN pip install git+https://github.com/topicaxis/trained-models.git@0.4.0

EXPOSE 8022

COPY ./docker-entrypoint.sh /app
ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["run"]