import unittest

from injectme import (
    InjectionFailure,
    inject,
    clear_dependencies,
    register,
    register_factory,
)

from .example_dep import DependencyA, FactoryA


class TestSimpleAPI(unittest.TestCase):
    def setUp(self):
        clear_dependencies()

    def test_instance_injection(self):
        @inject
        class SomeClass:
            dep: DependencyA

        instance = DependencyA()
        register(DependencyA, instance)
        some_class = SomeClass()

        self.assertIs(instance, some_class.dep)

    def test_factory_injection(self):
        @inject
        class SomeClass:
            dep: DependencyA

        factory = FactoryA()
        register_factory(DependencyA, factory)
        some_class = SomeClass()

        self.assertIs(factory.instance, some_class.dep)


    def test_clearing_dependencies(self):
        @inject
        class SomeClass:
            dep: DependencyA

        instance = DependencyA()
        register(DependencyA, instance)
        some_class = SomeClass()

        self.assertIs(instance, some_class.dep)

        clear_dependencies()
        with self.assertRaises(InjectionFailure):
            some_class = SomeClass()
