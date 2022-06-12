import unittest

from injectme import (
    InjectionFailure,
    InjectionNotSupported,
    Injector,
    DependenciesRegistry,
)

from .example_dep import (
    DependencyA,
    DependencyB,
    FactoryA,
)


class TestBasicInjecting(unittest.TestCase):
    def setUp(self):
        self.injector = Injector()
        self.registry = self.injector.registry

    def test_instance_injection(self):
        class SomeClass:
            dep: DependencyA


        self.injector(SomeClass)

        instance = DependencyA()
        self.registry.register_instance(DependencyA, instance)

        some_class = SomeClass()

        self.assertIs(instance, some_class.dep)

    def test_factory_injection(self):
        class SomeClass:
            dep: DependencyA


        self.injector(SomeClass)

        factory = FactoryA()
        self.registry.register_factory(DependencyA, factory)

        some_class = SomeClass()

        self.assertIs(factory.instance, some_class.dep)

    def test_dependency_available_in_init(self):
        class SomeClass:
            dep: DependencyA

            def __init__(self):
                self.init_dep = self.dep


        self.injector(SomeClass)

        factory = FactoryA()
        self.registry.register_factory(DependencyA, factory)

        some_class = SomeClass()

        self.assertIs(factory.instance, some_class.dep)
        self.assertIs(factory.instance, some_class.init_dep)

    def test_injection_fail(self):
        class SomeClass:
            dep_a: DependencyA


        self.injector(SomeClass)

        with self.assertRaises(InjectionFailure):
            some_class = SomeClass()

    def test_unsupported_injection_target(self):
        def some_func():
            pass


        with self.assertRaises(InjectionNotSupported):
            self.injector(some_func)

    def test_custom_registry(self):
        registry = DependenciesRegistry()
        injector = Injector(registry)

        injector.registry is registry

    def test_injector_as_decorator(self):
        injector = self.injector

        @injector
        class SomeClass:
            dep: DependencyA


        instance = DependencyA()
        self.registry.register_instance(DependencyA, instance)

        some_class = SomeClass()

        self.assertIs(instance, some_class.dep)


class TestAdvandedInjecting(unittest.TestCase):
    def test_custom_registry_injection(self):
        class SomeClass:
            dep: DependencyA


        registry = DependenciesRegistry()
        injector = Injector(registry)

        injector(SomeClass)

        instance = DependencyA()
        registry.register_instance(DependencyA, instance)

        some_class = SomeClass()

        self.assertIs(instance, some_class.dep)

    def test_multiple_injectors(self):
        injector_a = Injector()
        injector_b = Injector()

        class SomeBaseClass:
            dep_a: DependencyA

        class SomeDerivedClass(SomeBaseClass):
            dep_b: DependencyB


        injector_a(SomeBaseClass)
        injector_b(SomeDerivedClass)

        instance_a = DependencyA()
        injector_a.registry.register_instance(DependencyA, instance_a)

        instance_b = DependencyB()
        injector_b.registry.register_instance(DependencyB, instance_b)

        some_base_class = SomeBaseClass()
        self.assertIs(instance_a, some_base_class.dep_a)

        some_derived_class = SomeDerivedClass()
        self.assertIs(instance_a, some_derived_class.dep_a)
        self.assertIs(instance_b, some_derived_class.dep_b)

    def test_multidependency_injection(self):
        injector = Injector()
        registry = injector.registry

        class SomeClass:
            dep_a: DependencyA
            dep_b: DependencyB

        injector(SomeClass)

        factory_a = FactoryA()
        instance_b = DependencyB()

        registry.register_factory(DependencyA, factory_a)
        registry.register_instance(DependencyB, instance_b)
        some_class = SomeClass()

        self.assertIs(factory_a.instance, some_class.dep_a)
        self.assertIs(instance_b, some_class.dep_b)

    def test_inheritance_injection(self):
        injector = Injector()
        registry = injector.registry

        class SomeBaseClass:
            dep_a: DependencyA

        class SomeDerivedClass(SomeBaseClass):
            dep_b: DependencyB


        injector(SomeBaseClass)
        injector(SomeDerivedClass)

        instance_a = DependencyA()
        instance_b = DependencyB()
        registry.register_instance(DependencyA, instance_a)
        registry.register_instance(DependencyB, instance_b)

        some_base_class = SomeBaseClass()
        self.assertIs(instance_a, some_base_class.dep_a)

        some_derived_class = SomeDerivedClass()
        self.assertIs(instance_a, some_derived_class.dep_a)
        self.assertIs(instance_b, some_derived_class.dep_b)

    def test_super_initializes_parent_dependency(self):
        injector = Injector()
        registry = injector.registry

        class SomeBaseClass:
            dep_a: DependencyA

            def __init__(self):
                self.init_dep_a = self.dep_a

        class SomeDerivedClass(SomeBaseClass):
            dep_b: DependencyB

            def __init__(self):
                super().__init__()
                self.init_dep_aa = self.dep_a
                self.init_dep_b = self.dep_b

        injector(SomeBaseClass)
        injector(SomeDerivedClass)

        instance_a = DependencyA()
        instance_b = DependencyB()
        registry.register_instance(DependencyA, instance_a)
        registry.register_instance(DependencyB, instance_b)

        some_derived_class = SomeDerivedClass()
        self.assertIs(instance_a, some_derived_class.init_dep_a)
        self.assertIs(instance_a, some_derived_class.init_dep_aa)
        self.assertIs(instance_b, some_derived_class.init_dep_b)

    def test_lack_of_super_does_not_initialize_dependency(self):
        injector = Injector()
        registry = injector.registry

        class SomeBaseClass:
            dep_a: DependencyA

        class SomeDerivedClass(SomeBaseClass):
            dep_b: DependencyB

            def __init__(self):
                pass

        injector(SomeBaseClass)
        injector(SomeDerivedClass)

        instance_a = DependencyA()
        instance_b = DependencyB()
        registry.register_instance(DependencyA, instance_a)
        registry.register_instance(DependencyB, instance_b)

        some_derived_class = SomeDerivedClass()
        self.assertIs(instance_b, some_derived_class.dep_b)

        with self.assertRaises(AttributeError):
            getattr(some_derived_class, "dep_a")
