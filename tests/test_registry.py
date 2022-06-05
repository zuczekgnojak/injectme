import unittest

from injectme import (
    DependenciesRegistry,
    DependencyAlreadyRegistered,
    DependencyNotFound,
)

from .example_dep import Dependency, Factory


class TestRegistry(unittest.TestCase):
    def test_instantiation(self):
        DependenciesRegistry()

    def test_register_instance(self):
        instance = Dependency()
        registry = DependenciesRegistry()

        registry.register_instance(Dependency, instance)
        result = registry.get(Dependency)

        self.assertIs(result, instance)

    def test_register_factory(self):
        registry = DependenciesRegistry()
        factory = Factory()

        registry.register_factory(Dependency, factory)

        result = registry.get(Dependency)
        self.assertIs(result, factory.instance)

    def test_register_instance_twice(self):
        instance_a = Dependency()
        instance_b = Dependency()

        registry = DependenciesRegistry()
        registry.register_instance(Dependency, instance_a)
        with self.assertRaises(DependencyAlreadyRegistered):
            registry.register_instance(Dependency, instance_b)

    def test_register_factory_twice(self):
        factory_a = Factory()
        factory_b = Factory()

        registry = DependenciesRegistry()
        registry.register_factory(Dependency, factory_a)
        with self.assertRaises(DependencyAlreadyRegistered):
            registry.register_instance(Dependency, factory_b)

    def test_register_instance_factory(self):
        factory = Factory()
        instance = Dependency()
        registry = DependenciesRegistry()

        registry.register_factory(Dependency, factory)
        with self.assertRaises(DependencyAlreadyRegistered):
            registry.register_instance(Dependency, instance)

    def test_dependency_not_registered(self):
        registry = DependenciesRegistry()
        with self.assertRaises(DependencyNotFound):
            registry.get(Dependency)
