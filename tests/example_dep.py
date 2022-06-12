class DependencyA:
    pass


class DependencyB:
    pass


class FactoryA:
    def __init__(self):
        self.instance = DependencyA()

    def __call__(self):
        return self.instance
