.. build-dashboard documentation master file, created by
   sphinx-quickstart on Sun May  5 15:29:11 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to build-dashboard's documentation!
===========================================

build-dashboard is an open-source client for Buildbot that allows for reviewing builds in the terminal.

How to run
-------------

.. code-block:: bash

    build_dashboard  --protocol https --host buildbot.example.com

Configuration file
-------------------

build_dashboard looks for a TOML-based `.buildbotrc` in the users home directory. If it finds one it, it will use the parameters in the file. Any arguments passed on the command line will override the configuration file.

Example configuration file:

.. code-block:: ini

    protocol = "http"
    host = "localhost"
    unix = "/var/run/buildbot.sock"


.. toctree::
   :maxdepth: 1
   :caption: Contents:
   
   modules



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
