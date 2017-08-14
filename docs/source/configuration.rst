Configuration
=============

Basic configuration
-------------------

Classifier can be configured by creating a file called *settings.py*. The following
configuration variables must always be set.

.. py:data:: HOST

   The IP address that Classifier will bind to

   Type: ``string``

.. py:data:: PORT

   The port that Classifier will listen to

   Type: ``int``

.. py:data:: SECRET_KEY

   The secret key that will be used by Flask

   Type: ``string``

.. py:data:: CLASSIFIERS

   A dictionary with the supported classifiers. For more info see the ``"setting up the classifiers"``
   section of the documentation

   Type: ``dict``


Optional configuration variables
--------------------------------

These configuration variables are optional.

.. py:data:: DEBUG

   Run the application in debug mode.

   Default: ``False``


.. py:data:: LOGGING

   The dictionary with the configuration settings for the python logger

   Default: ``None``

.. py:data:: LOG_FILE

   The path to the log log file. By default logging to file is disabled.

   Default: ``None``

.. py:data:: LOG_FILE_COUNT

   The number of log files to keep if they have exceeded their maximum size

   Default: ``5``

.. py:data:: LOG_FILE_MAX_SIZE

   The maximum log file size in bytes

   Default: ``1000000``

.. py:data:: CONSUL_HOST

   The address of the Consul server.

.. py:data:: CONSUL_PORT

   The port that the Consul server listens to.

   Default: ``8500``

.. py:data:: CONSUL_SCHEME

   The scheme to use when a connection to Consul is made. Valid values are
   'http' and 'https'.

   Default: ``http``

.. py:data:: CONSUL_VERIFY_SSL

   Verify ssl for the Consul connection.

   Default: ``True``

.. py:data:: CONSUL_HEALTH_INTERVAL

   The interval that Consul will use for the health check.

   Default: ``10s``

.. py:data:: CONSUL_HEALTH_TIMEOUT

   The time after which Consul will assume a timeout has occurred.

   Default: ``5s``

.. py:data:: WORKER_MAX_REQUESTS

   The number of requests each worker will service before restarting.

   Default: ``100``

.. py:data:: WORKER_MAX_REQUESTS_JITTER

   The jitter value that will be used for the maximum number of request that
   every worker will service before restarting.

   Default: ``10``

.. py:data:: WORKERS

   The number of workers to start.

   Default: ``2``


Setting up the classifiers
--------------------------

The ``CLASSIFIERS`` configuration variable contains the trained category models that are
used by TopicAxis. You can download them from the following repository

.. code-block:: shell

   git clone https://github.com/topicaxis/trained-models

Add the following code snipped to the ``settings.py`` file in order to load the trained models.

.. code-block:: python

   CLASSIFIERS = {
      "categories": Classifier(
           data_extractor=extract_text_data,
           classifier="/path/to/pipeline.pickle",
           result_processor=lambda result: {"categories": result},
           probabilities=True
       )
   }

Consul configuration
--------------------

Classifier instances are required to register with a service discovery application.
Consul has been selected this purpose. The configuration variables with the appropriate
values for the Consul server have to be added in the ``settings.py`` file.

.. code-block:: python

   CONSUL_HOST = "192.168.1.105"
   CONSUL_PORT = 8500
   CONSUL_SCHEME = "https"
   CONSUL_VERIFY_SSL = True
   CONSUL_HEALTH_INTERVAL = "10s"
   CONSUL_HEALTH_TIMEOUT = "5s"

Tyk gateway configuration
-------------------------

Classifier doesn't have a built-in authentication mechanism. The tyk API gateway
is used to serve that purpose. Create a configuration file in Tyk's app configuration
folder with the required settings like the following example.

.. code-block:: json

   {
       "name": "Classifier API",
       "slug": "classifier-api",
       "api_id": "1",
       "org_id": "1",
       "definition": {
           "location": "header",
           "key": "x-api-version"
       },
       "auth": {
           "use_param": false,
           "param_name": "",
           "use_cookie": false,
           "cookie_name": "",
           "auth_header_name": "authorization"
       },
       "version_data": {
           "not_versioned": true,
           "versions": {
               "Default": {
                   "name": "Default",
                   "expires": "",
                   "use_extended_paths": true,
                   "extended_paths": {
                       "ignored": null,
                       "white_list": null,
                       "black_list": null
                   }
               }
           }
       },
       "proxy": {
           "listen_path": "/classifier",
           "target_url": "http://services.example.com",
           "strip_listen_path": true,
           "enable_load_balancing": true,
           "service_discovery": {
               "use_discovery_service": true,
               "query_endpoint": "http://<consul-address>:<consul-port>/v1/catalog/service/web?passing",
               "use_nested_query": false,
               "parent_data_path": "",
               "data_path": "Address",
               "port_data_path": "ServicePort",
               "target_path": "",
               "use_target_list": true,
               "cache_timeout": 10,
               "endpoint_returns_list": true
           }
       },
       "enable_batch_request_support": false
   }

Replace the ``<consul-host>`` and ``<consul-port>`` the the IP address and port
of the Consul server so that it is possible for Tyk to find the available
Classifier instances. The ``<target_url>`` should also be replaced with a more
appropriate domain.

With the above configuration it will be possible to execute an authenticated Classifier
request on ``http://services.example.com/classifier`` using an API key that was created
with Tyk.

Nginx configuration
-------------------

Nginx needs to be configured to forward traffic for the domain name that will be used by Classifier to Tyk.
Add a configuration file for Classifierin the ``sites-available`` configuration folder of nginx
and create a symbolic link for this file to the ``sites-enabled`` folder.

.. code-block:: nginx

   server {
       listen 80;
       server_name classifier.example.com;

       location / {
               rewrite ^/(.*)$ /classifier/$1 break;
               proxy_pass_header Server;
               proxy_set_header Host services.example.com;
               proxy_redirect off;
               proxy_set_header X-Real-IP $remote_addr;
               proxy_set_header X-Scheme $scheme;
               proxy_pass http://tyk;
       }
   }

Replace ``server_name`` with the domain that you want to use to access Classifier and
``proxy_set_header`` with the domain that you have configured Tyk to listen to.

You also need to modify the ``proxy_pass`` variable with the appropriate upstream server

.. toctree::
   :maxdepth: 1
