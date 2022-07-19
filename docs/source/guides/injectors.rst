Injector
========

The :py:class:`injectme.Injector` is on of the two core classes used by injectme.
Injector's responsiblity is to perform injection on specified class using dependencies
from :py:class:`injectme.DependenciesRegistry`.

:py:class:`injectme.Injector` is a callable acting like a class decorator and can be used
as such. Each decorated class will have it's dependencies assigned as an instance attributes
just before calling the :py:func:`__init__` method.

The :py:func:`injectme.inject` function is a shortcut for calling appropriate methods on a
single global :class:`Injector` instance created by injectme to provide :doc:`simple_api`.


:py:class:`injectme.Injector` can be created using custom registry. If there's no registry
passed to :py:func:`__init__`, new instance :py:class:`injectme.DependenciesRegistry` is automatically
created and can be reached by using :py:func:`injectme.Injector.registry` property.

Example:
~~~~~~~~
.. code-block:: python
    :caption: example.py

    from injectme import Injector


    class Dependency:
        def __init__(self, name):
            self.name = name


    injector = Injector()

    # used as a decorator
    @injector
    class ExampleA:
        dep: Dependency

        def show_dep(self):
            print(f"I am A and I have dependency {self.dep.name}")


    class ExampleB:
        dep: Dependency

        def show_dep(self):
            print(f"I am B and I have dependency {self.dep.name}")


    # or a simple callable
    injector(ExampleB)


    # dependencies have to be registered before instantiating depending
    # classes
    injector.registry.register_instance(
        Dependency, Dependency("some-dep")
    )

    ExampleA().show_dep()
    ExampleB().show_dep()


.. code-block:: shell

    $ python3 example.py

    I am A and I have dependency some-dep
    I am B and I have dependency some-dep new dependency
