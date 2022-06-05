import unittest

from injectme import (
    DependenciesRegistry,
    inject,
    register,
    register_factory,
)
from injectme.global_registry import _reset_registry


class DependencyA:
    pass


class DependencyB:
    pass


class FactoryA:
    def __init__(self):
        self.instance = DependencyA

    def __call__(self):
        return self.instance


class TestAdvancedInjecting(unittest.TestCase):
    def setUp(self):
        _reset_registry()

    def test_multidependency_injection(self):
        @inject
        class SomeClass:
            dep_a: DependencyA
            dep_b: DependencyB

        factory_a = FactoryA()
        instance_b = DependencyB()

        register_factory(DependencyA, factory_a)
        register(DependencyB, instance_b)
        some_class = SomeClass()

        self.assertIs(factory_a.instance, some_class.dep_a)
        self.assertIs(instance_b, some_class.dep_b)

    def test_inheritance_injection(self):
        @inject
        class SomeBaseClass:
            dep_a: DependencyA

        @inject
        class SomeDerivedClass(SomeBaseClass):
            dep_b: DependencyB

        instance_a = DependencyA()
        instance_b = DependencyB()
        register(DependencyA, instance_a)
        register(DependencyB, instance_b)

        some_base_class = SomeBaseClass()
        self.assertIs(instance_a, some_base_class.dep_a)

        some_derived_class = SomeDerivedClass()
        self.assertIs(instance_a, some_derived_class.dep_a)
        self.assertIs(instance_b, some_derived_class.dep_b)

    def test_custom_registry(self):
        registry = DependenciesRegistry()

        @inject(registry)
        class SomeBaseClass:
            dep_a: DependencyA

        @inject(registry)
        class SomeDerivedClass(SomeBaseClass):
            dep_b: DependencyB

        instance_a = DependencyA()
        instance_b = DependencyB()
        registry.register_instance(DependencyA, instance_a)
        registry.register_instance(DependencyB, instance_b)

        some_base_class = SomeBaseClass()
        self.assertIs(instance_a, some_base_class.dep_a)

        some_derived_class = SomeDerivedClass()
        self.assertIs(instance_a, some_derived_class.dep_a)
        self.assertIs(instance_b, some_derived_class.dep_b)

    def test_multiregistry(self):
        registry_a = DependenciesRegistry()
        registry_b = DependenciesRegistry()

        @inject(registry_a)
        class SomeBaseClass:
            dep_a: DependencyA

        @inject(registry_b)
        class SomeDerivedClass(SomeBaseClass):
            dep_b: DependencyB

        instance_a = DependencyA()
        registry_a.register_instance(DependencyA, instance_a)

        instance_b = DependencyB()
        registry_b.register_instance(DependencyB, instance_b)

        some_base_class = SomeBaseClass()
        self.assertIs(instance_a, some_base_class.dep_a)

        some_derived_class = SomeDerivedClass()
        self.assertIs(instance_a, some_derived_class.dep_a)
        self.assertIs(instance_b, some_derived_class.dep_b)

    def test_super_initializes_parent_dependency(self):
        @inject
        class SomeBaseClass:
            dep_a: DependencyA

            def __init__(self):
                self.init_dep_a = self.dep_a

        @inject
        class SomeDerivedClass(SomeBaseClass):
            dep_b: DependencyB

            def __init__(self):
                super().__init__()
                self.init_dep_aa = self.dep_a
                self.init_dep_b = self.dep_b

        instance_a = DependencyA()
        instance_b = DependencyB()
        register(DependencyA, instance_a)
        register(DependencyB, instance_b)

        some_derived_class = SomeDerivedClass()
        self.assertIs(instance_a, some_derived_class.init_dep_a)
        self.assertIs(instance_a, some_derived_class.init_dep_aa)
        self.assertIs(instance_b, some_derived_class.init_dep_b)

    def test_lack_of_super_does_not_initialize_dependency(self):
        @inject
        class SomeBaseClass:
            dep_a: DependencyA

        @inject
        class SomeDerivedClass(SomeBaseClass):
            dep_b: DependencyB

            def __init__(self):
                pass

        instance_a = DependencyA()
        instance_b = DependencyB()
        register(DependencyA, instance_a)
        register(DependencyB, instance_b)

        some_derived_class = SomeDerivedClass()
        self.assertIs(instance_b, some_derived_class.dep_b)

        with self.assertRaises(AttributeError):
            getattr(some_derived_class, "dep_a")
