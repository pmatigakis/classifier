Installation
============

Third party requirements
------------------------

The following applications are required. Classifier will probably run with newer
versions of those dependencies.

* Nginx
* tyk gateway v2.3.5
* Consul v0.8.3

Installing using virtualenv
---------------------------
Classifier should be installed using virtualenv. Create and activate a python
virtual environment.

.. code-block:: shell

   virtualenv --python=python2.7 virtualenv
   source virtualenv/bin/activate

Download the Classifier source code. This example will download the latest
development source code. It is better to use a stable version in production.

.. code-block:: shell

   git clone https://github.com/topicaxis/classifier.git

Install Classifier.

.. code-block:: shell

   python setup.py install

.. toctree::
   :maxdepth: 1
