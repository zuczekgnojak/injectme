import unittest

from injectme import (
    DependenciesRegistry,
    get_registry,
    register,
    register_factory,
    set_registry,
)
from injectme.global_registry import _get_current_global_registry, _reset_registry

from .example_dep import Dependency, Factory


class TestGlobalRegistry(unittest.TestCase):
    def setUp(self):
        _reset_registry()

    def test_auto_create(self):
        self.assertIsNone(_get_current_global_registry())

        registry = get_registry()

        self.assertIsInstance(registry, DependenciesRegistry)
        self.assertIs(registry, get_registry())
        self.assertIs(registry, _get_current_global_registry())

    def test_setting_global_registry(self):
        self.assertIsNone(_get_current_global_registry())

        registry = DependenciesRegistry()
        set_registry(registry)

        self.assertIs(registry, get_registry())
        self.assertIs(registry, _get_current_global_registry())

    def test_registering_global_instance(self):
        instance = Dependency()
        register(Dependency, instance)

        registry = get_registry()
        result = registry.get(Dependency)
        self.assertIs(instance, result)

    def test_registering_global_factory(self):
        factory = Factory()
        register_factory(Dependency, factory)

        registry = get_registry()
        result = registry.get(Dependency)
        self.assertIs(factory.instance, result)
