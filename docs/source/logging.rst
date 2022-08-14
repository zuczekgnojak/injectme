Logging
=======

injectme is using :code:`NullHandler` pattern for libraries which is described here
https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library. As a result
you will not see any logging output from injectme without providing configuration.

Currently, there are only :code:`DEBUG` level messages logged by the injectme so there's no point in
configuring any other logging level for it.

Below you'll find sample logging configuration, a piece of code using it and logging output.

Example:
~~~~~~~~

.. code-block:: python
    :caption: example.py

    from logging.config import dictConfig

    from injectme import inject, register, clear_dependencies

    logconf = {
        "version": 1,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            },
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "injectme": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": False,
            },
        }
    }

    dictConfig(logconf)


    class Dependency:
        pass


    @inject
    class Service:
        dependency: Dependency

    register(Dependency, Dependency())

    Service()

    clear_dependencies()


.. code-block:: shell

    $ python3 example.py

    2022-08-14 21:37:01,552 [DEBUG] injectme.injector: marking <class '__main__.Service'> as target for <injectme.injector.Injector object at 0x7fd798b8b940>
    2022-08-14 21:37:01,552 [DEBUG] injectme.registry: registering <__main__.Dependency object at 0x7fd798b8bb50> as <class '__main__.Dependency'> dependency in <injectme.registry.DependenciesRegistry object at 0x7fd798b8b970>
    2022-08-14 21:37:01,553 [DEBUG] injectme.injector: injecting into <__main__.Service object at 0x7fd798b8bc10> by <injectme.injector.Injector object at 0x7fd798b8b940> using <injectme.registry.DependenciesRegistry object at 0x7fd798b8b970>
    2022-08-14 21:37:01,553 [DEBUG] injectme.registry: looking for <class '__main__.Dependency'> in <injectme.registry.DependenciesRegistry object at 0x7fd798b8b970>
    2022-08-14 21:37:01,553 [DEBUG] injectme.registry: clearing <injectme.registry.DependenciesRegistry object at 0x7fd798b8b970> registry
