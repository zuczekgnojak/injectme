from .errors import (
    DependencyNotFound,
    InjectionFailure,
    InjectionNotSupported,
)
from .registry import DependenciesRegistry


class Injector:
    def __init__(self, registry=None):
        if registry is None:
            registry = DependenciesRegistry()

        self._registry = registry

    @property
    def registry(self):
        return self._registry

    def __call__(self, cls):
        if not isinstance(cls, type):
            raise InjectionNotSupported(cls)

        injector = self

        def __init_deps__(self):
            annotations = cls.__dict__.get("__annotations__", {})
            registry = injector.registry

            try:
                for name, dependency in annotations.items():
                    instance = registry.get(dependency)
                    setattr(self, name, instance)
            except DependencyNotFound as err:
                raise InjectionFailure(cls) from err

        def injectme_init(self, *args, **kwargs):
            cls.__init_deps__(self)
            cls.__original_init__(self, *args, **kwargs)

        cls.__original_init__ = cls.__init__
        cls.__init_deps__ = __init_deps__
        cls.__init__ = injectme_init

        return cls
