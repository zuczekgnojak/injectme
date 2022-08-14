Simple API
==========

If you don't want to dive into the details of "Injectors" and "Registries" you
can use a subset of `injectme`'s capabilities called "Simple API".

The "Simple API" consists of 4 functions: :py:func:`injectme.inject`,
:py:func:`injectme.register`, :py:func:`injectme.register_factory` and
:py:func:`injectme.clear_dependencies`.

These functions are simply wrapping calls to single, global instance of
:py:class:`injectme.Injector`.

Example:
~~~~~~~~

.. code-block:: python
    :caption: example.py

    from injectme import (
        inject,
        register,
        register_factory,
        clear_dependencies,
    )


    class DependencyA:
        def __init__(self, name):
            self.name = name

        def __str__(self):
            return f"DependencyA: {self.name}"


    class DependencyB:
        def __init__(self, name):
            self.name = name

        def __str__(self):
            return f"DependencyB: {self.name}"


    # using inject to mark this class as a target for DI
    @inject
    class Example:
        dep_a: DependencyA
        dep_b: DependencyB

        def print_deps(self):
            print("Showing dependencies:")
            print(self.dep_a)
            print(self.dep_b)


    # now it's time for setting up the injection

    # register single instance for DependencyA
    register(DependencyA, DependencyA("Alice"))

    # register factory for DependencyB
    def dep_b_factory():
        return DependencyB("Bob")

    register_factory(DependencyB, dep_b_factory)

    # see how it works
    print("Creating Example instance")
    example = Example()
    example.print_deps()


    # clear all deps and see how it breaks
    print("Clearing dependencies")
    clear_dependencies()
    Example()


.. code-block:: shell

    $ python3 example.py

    Creating Example instance
    Showing dependencies:
    DependencyA: Alice
    DependencyB: Bob
    Clearing dependencies
    Traceback (most recent call last):
        ...
    injectme.errors.InjectionFailure: Failed to inject dependencies into <class '__main__.Example'>
