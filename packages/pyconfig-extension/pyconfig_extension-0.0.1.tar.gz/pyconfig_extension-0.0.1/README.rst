
===============
Configuration Manager for Python
===============


Python Configuration
********************************

This library is designed for managing Configuration in Python projects and is inspired by
the Microsoft.Extensions.Configuration library in C#.

Installation
------------

This library can be installed via pip:

.. code-block:: bash

    pip install pyconfig

Usage
-----
To use the configuration manager, you first need to create a `ConfigurationBuilder`
object and add one or more configuration sources.
For example, you can add a JSON file source and an environment variable source like this:

.. code-block:: python

    from pyconfig import ConfigurationBuilder, IConfigurationBuilder

    builder: IConfigurationBuilder = ConfigurationBuilder() \
        .add_json_file('config.json') \
        .add_environment_variables()

    config = builder.build()


