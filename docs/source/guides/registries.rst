Registry
========

The :py:class:`injectme.DependenciesRegistry` is on of the two core classes used by injectme.
Registry's responsiblity is to store instances and factories for registered dependencies.

The :py:func:`injectme.register`, :py:func:`injectme.register_factory` and
:py:func:`injectme.clear_dependencies` are all shortcuts for calling appropriate methods on a
single global :py:class:`DependenciesRegistry` instance created by injectme to provide
:doc:`simple_api`.

You can create your own instance of :py:class:`DependenciesRegistry`. It's not very usefule on it's
own but provides foundation of dependencies management for :py:class:`injectme.Injector`.

Example:
~~~~~~~~
.. code-block:: python
    :caption: example.py

    from injectme import (
        DependenciesRegistry,
        DependencyNotFound,
        DependencyAlreadyRegistered,
    )

    class DependencyA:
        pass


    class DependencyB:
        pass


    registry = DependenciesRegistry()

    # there's no dependencies registered so we'll get an
    # exception trying to get one
    try:
        registry.get(DependencyA)
    except DependencyNotFound as err:
        print("Dependency not found:")
        print(err)


    # let's register an instance
    dep_a = DependencyA()
    registry.register_instance(DependencyA, dep_a)

    # and with 'get()' call we can get same instance from the registry
    print("Getting DependencyA")
    registered_dep_a = registry.get(DependencyA)
    print("Got same instance?", dep_a is registered_dep_a)


    # let's register a factory
    def dep_b_factory():
        print("Creating DependencyB")
        return DependencyB()

    registry.register_factory(DependencyB, dep_b_factory)

    # same as before, use 'get()' to get instance of registered dependency
    print("Getting DependencyB")
    dep_b_1 = registry.get(DependencyB)
    dep_b_2 = registry.get(DependencyB)

    # the factory is being called for each 'get()'
    print("Got same instance?", dep_b_1 is dep_b_2)


    # trying to register same dependency twice
    try:
        registry.register_instance(DependencyA, DependencyA())
    except DependencyAlreadyRegistered as err:
        print("Dependency already registered:")
        print(err)


    # clearing registry
    print("Clear registry")
    registry.clear()

    try:
        registry.get(DependencyA)
    except DependencyNotFound as err:
        print("Dependency not found:")
        print(err)



.. code-block:: shell

    $ python3 example.py

    Dependency not found:
    Dependency <class '__main__.DependencyA'> has not been found in the registry

    Getting DependencyA
    Got same instance? True

    Getting DependencyB
    Creating DependencyB
    Creating DependencyB
    Got same instance? False

    Dependency already registered:
    Dependency <class '__main__.DependencyA'> already registered

    Clear registry
    Dependency not found:
    Dependency <class '__main__.DependencyA'> has not been found in the registry
