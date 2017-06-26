Running
=======

Running using supervisor
------------------------

Classifier should be run using ``supervisor``. A basic configuration file like
the following can be used.

.. code-block:: ini

   [program:classifier]
   command=/path/to/virtualenv/bin/classifier-cli runserver
   directory=/path/to/settings
   autostart=true
   autorestart=unexpected
   exitcodes=0,2
   user=john
   stdout_logfile=/path/to/logs/stdout.log
   stdout_logfile_maxbytes=1MB
   stdout_logfile_backups=10
   stderr_logfile=/path/to/logs/stderr.log
   stderr_logfile_maxbytes=1MB
   stderr_logfile_backups=10


.. toctree::
   :maxdepth: 1
