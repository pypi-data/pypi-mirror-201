logging42
=========

A configuration for the loguru (https://github.com/Delgan/loguru) logger.

It is important that it be the first import to run so the standard logging basicConfig method has an effect.

Features
--------

- Stderr output

- intercepted logging from client libraries

- Disabled better exceptions for log levels above debug to mitigate secret leaking

- Configuration retriever which safely logs retrieved values

Installation
------------

.. code:: bash

   pip install logging42


Examples
--------

**main.py**

.. code:: python

    from logging42 import logger

    logger.debug('hello world)
