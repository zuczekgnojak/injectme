API Reference
=============

.. contents:: Table of Contents
    :depth: 3
    :local:



Constants
---------

injectme.__version__
~~~~~~~~~~~~~~~~~~~~

Current injectme's version.

    >>> import injectme
    >>> injectme.__version__
    '0.0.5'


Functions
---------

.. note::
    These functions compose "simplified API". They are wrappers
    over methods of single :class:`injectme.Injector` instance.


injectme.inject
~~~~~~~~~~~~~~~
.. autofunction:: injectme.inject

    It can be used either as a function or as a decorator. All of the class annotations will be inspected
    and provided during object instantiation.

    Classes marked for injection will have their dependencies
    set just before calling their ``__init__``.

    Dependencies used during injection phase should be registered
    with either :func:`injectme.register` or :func:`injectme.register_factory` before instantiating
    any class which needs them.

        >>> from injectme import inject, register
        >>> class UsersRepository:
        ...     def get_user(self):
        ...         return ("john", "doe")
        ...
        >>> @inject
        ... class UsersService:
        ...     users_repo: UsersRepository
        ...
        ...     def run(self):
        ...         print(self.users_repo.get_user())
        ...
        >>> register(UsersRepository, UsersRepository())
        >>> UsersService().run()
        ('john', 'doe')

    If you fail to register all of the dependencies of a class
    you are trying to instantiate the :exc:`injectme.InjectionFailure` will
    be raised.

        >>> from injectme import inject
        >>> class Dependency:
        ...     ...
        ...
        >>> @inject
        ... class SomeClass:
        ...     dep: Dependency
        ...
        >>> SomeClass()
        Traceback (most recent call last):
            ...
        injectme.errors.InjectionFailure: ...

    .. note::
        This function is a wrapper for :func:`injectme.Injector.__call__`.

injectme.register
~~~~~~~~~~~~~~~~~
.. autofunction:: injectme.register

    .. note::
        This function is a wrapper for :func:`injectme.DependenciesRegistry.register_instance`.

injectme.register_factory
~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: injectme.register_factory

    .. note::
        This function is a wrapper for :func:`injectme.DependenciesRegistry.register_factory`.

injectme.clear_dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: injectme.clear_dependencies

    .. note::
        This function is a wrapper for :func:`injectme.DependenciesRegistry.clear`.



Classes
-------

injectme.DependenciesRegistry
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: injectme.DependenciesRegistry
   :members: get, register_instance, register_factory, clear

injectme.Injector
~~~~~~~~~~~~~~~~~
.. autoclass:: injectme.Injector
   :members: __init__, registry, __call__



Exceptions
----------

injectme.InjectmeException
~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoexception:: injectme.InjectmeException

injectme.DependencyNotFound
~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoexception:: injectme.DependencyNotFound

injectme.DependencyAlreadyRegistered
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoexception:: injectme.DependencyAlreadyRegistered

injectme.InjectionNotSupported
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoexception:: injectme.InjectionNotSupported

injectme.InjectionFailure
~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoexception:: injectme.InjectionFailure
