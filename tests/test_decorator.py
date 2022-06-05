import unittest

from injectme import (
    InjectionFailure,
    InjectionNotSupported,
    inject,
    register,
    register_factory,
)
from injectme.global_registry import _reset_registry

from .example_dep import Dependency, Factory


class TestBasicInjecting(unittest.TestCase):
    def setUp(self):
        _reset_registry()

    def test_instance_injection(self):
        @inject
        class SomeClass:
            dep: Dependency

        instance = Dependency()
        register(Dependency, instance)
        some_class = SomeClass()

        self.assertIs(instance, some_class.dep)

    def test_factory_injection(self):
        @inject
        class SomeClass:
            dep: Dependency

        factory = Factory()
        register_factory(Dependency, factory)
        some_class = SomeClass()

        self.assertIs(factory.instance, some_class.dep)

    def test_dependency_available_in_init(self):
        @inject
        class SomeClass:
            dep: Dependency

            def __init__(self):
                self.init_dep = self.dep

        factory = Factory()
        register_factory(Dependency, factory)
        some_class = SomeClass()

        self.assertIs(factory.instance, some_class.dep)
        self.assertIs(factory.instance, some_class.init_dep)

    def test_injection_fail(self):
        @inject
        class SomeClass:
            dep_a: Dependency

        with self.assertRaises(InjectionFailure):
            some_class = SomeClass()

    def test_unsupported_injection_target(self):
        with self.assertRaises(InjectionNotSupported):

            @inject
            def some_func():
                pass
