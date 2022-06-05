class Dependency:
    pass


class Factory:
    def __init__(self):
        self.instance = Dependency()

    def __call__(self):
        return self.instance
