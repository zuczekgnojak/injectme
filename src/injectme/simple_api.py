from .injector import Injector

inject = Injector()


def _get_registry():
    return inject.registry


def register(dependency, instance):
    registry = _get_registry()
    registry.register_instance(dependency, instance)


def register_factory(dependency, factory):
    registry = _get_registry()
    registry.register_factory(dependency, factory)


def clear_dependencies():
    registry = _get_registry()
    registry.clear()
