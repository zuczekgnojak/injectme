Factories
=========

Registering the dependency's instance is not the only way of telling injectme
what object to use during "injection" phase. You can also register "factories",
simple callables returning instances of dependencies.

To register a factory instead of single instance use
:py:func:`injectme.register_factory` or :py:meth:`injectme.DependenciesRegistry.register_factory`.

The registered factory should not require any arguments. The returned value
will be set as an instance of corresponding dependency. The factory will be
called each time an instance is needed for injecting.

Example:
~~~~~~~~

.. code-block:: python
    :caption: example.py

    from injectme import inject, register_factory


    class Dependency:
        pass


    @inject
    class Example:
        dep: Dependency


    def dependency_factory():
        print("Creating new dependency")
        return Dependency()


    register_factory(Dependency, dependency_factory)

    print("First injection")
    Example()

    print("Second injection")
    Example()


.. code-block:: shell

    $ python3 example.py

    First injection
    Creating new dependency
    Second injection
    Creating new dependency
