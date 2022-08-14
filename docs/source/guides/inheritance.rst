Inheritance
===========

It is possible to use class marked as a target for injection as a parent class in inheritance.
If you want to add additional dependencies in the child class, it's possible. The only requirement is that
both parent and child are decorated by the :py:func:`injectme.inject` or :py:class:`injectme.Injector`.

The parent's dependencies are available to child as if they were its own attributes. It's good to take a
look at the :doc:`__init__` guide to better understand how this mechanism works.


Example:
~~~~~~~~
.. code-block:: python
    :caption: example.py

    from injectme import inject, register


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


    # base class has to be decorated using Injector
    @inject
    class BaseService:
        dep_a: DependencyA


    # derived class also needs to be decorated by Injector
    @inject
    class AdvancedService(BaseService):
        dep_b: DependencyB

        def print_deps(self):
            print("AdvancedService deps:")
            print(self.dep_a)
            print(self.dep_b)


    # register dependencies
    register(DependencyA, DependencyA("Alice"))
    register(DependencyB, DependencyB("Bob"))

    advanced_service = AdvancedService()
    advanced_service.print_deps()


.. code-block:: shell

    $ python3 example.py

    AdvancedService deps:
    DependencyA: Alice
    DependencyB: Bob
