__init__
========

The dependencies of a class are injected *before* calling it's :code:`__init__` method. It's perfectly fine
to use these dependencies during object's initialization.


Example #1:
~~~~~~~~~~~
.. code-block:: python
    :caption: example1.py

    from injectme import inject, register


    class Dependency:
        def __init__(self, name):
            self.name = name

        def __str__(self):
            return f"Dependency: {self.name}"


    @inject
    class Service:
        dep: Dependency

        def __init__(self):
            print("In Service __init__")
            print(self.dep)


    register(Dependency, Dependency("Debra"))

    service = Service()


.. code-block:: shell

    $ python3 example1.py

    In Service __init__
    Dependency: Debra


If you decide to use inheritance and implement custom :code:`__init__` methods you have to call parent's :code:`__init__` before
you can use dependencies declared there. If you do not call :code:`super().__init__()` you will get an error when
trying to access them.


Example #2:
~~~~~~~~~~~
.. code-block:: python
    :caption: example2.py

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


    register(DependencyA, DependencyA("Alice"))
    register(DependencyB, DependencyB("Bob"))


    @inject
    class BaseService:
        dep_a: DependencyA


    # after calling super().__init__() you can use deps without
    # any issue
    @inject
    class AdvancedService(BaseService):
        dep_b: DependencyB

        def __init__(self):
            super().__init__()
            print("AdvancedService __init__")
            print(self.dep_a)
            print(self.dep_b)


    advanced_service = AdvancedService()

    # if you try to access parent's dependency before calling its __init__
    # you'll get AttributeError
    @inject
    class AdvancedServiceBrokenInit(BaseService):
        dep_b: DependencyB

        def __init__(self):
            print("AdvancedService __init__")
            print(self.dep_a)
            print(self.dep_b)
            super().__init__()


    try:
        AdvancedServiceBrokenInit()
    except AttributeError as e:
        print(e)


    # you'll get same result if you completly forget about initializing parent
    @inject
    class AdvancedServiceMissingSuperInit(BaseService):
        dep_b: DependencyB

        def __init__(self):
            print("AdvancedServiceMissingSuperInit __init__")

        def print_deps(self):
            print("AdvancedServiceMissingSuperInit deps:")
            print(self.dep_a)
            print(self.dep_b)


    try:
        service = AdvancedServiceMissingSuperInit()
        service.print_deps()
    except AttributeError as e:
        print(e)



.. code-block:: shell

    $ python3 example2.py

    AdvancedService __init__
    DependencyA: Alice
    DependencyB: Bob

    AdvancedServiceBrokenInit __init__
    'AdvancedServiceBrokenInit' object has no attribute 'dep_a'

    AdvancedServiceMissingSuperInit __init__
    AdvancedServiceMissingSuperInit deps:
    'AdvancedServiceMissingSuperInit' object has no attribute 'dep_a'
