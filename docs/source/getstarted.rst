Get Started
===========

Install injectme
~~~~~~~~~~~~~~~~

.. code-block:: bash

    pip install injectme


Use it in your project
~~~~~~~~~~~~~~~~~~~~~~

Let's start with simple project:

.. code-block:: bash

    .
    └── src
        ├── app.py
        ├── bootstrap.py
        ├── cars.py
        └── users.py


.. code-block:: python
    :caption: Contents of src/users.py

    class UsersRepository:
    def __init__(self, users):
        self.users = users

    def get_users(self):
        return self.users


    class UsersService:
        def __init__(self, users_repo: UsersRepository):
            self.users_repo = users_repo

        def show_users(self):
            print(self.users_repo.get_users())


.. code-block:: python
    :caption: Contents of src/cars.py

    class CarsRepository:
        def __init__(self, cars):
            self.cars = cars

        def get_cars(self):
            return self.cars


    class CarsService:
        def __init__(self, cars_repo: CarsRepository):
            self.cars_repo = cars_repo

        def show_cars(self):
            print(self.cars_repo.get_cars())


.. code-block:: python
    :caption: Contents of src/app.py

    from .cars import CarsService
    from .users import UsersService


    class App:
        def __init__(
            self,
            cars_service: CarsService,
            users_service: UsersService,
        ):
            self.cars_service = cars_service
            self.users_service = users_service


.. code-block:: python
    :caption: Contents of src/bootstrap.py

    from .app import App
    from .cars import CarsRepository, CarsService
    from .users import UsersRepository, UsersService


    def bootstrap():
        cars_repository = CarsRepository(("cara", "carb"))
        cars_service = CarsService(cars_repository)

        users_repository = UsersRepository(("usera", "userb"))
        users_service = UsersService(users_repository)

        return App(
            cars_service=cars_service,
            users_service=users_service,
        )


There is no much code in here so it does not look that bad. Be aware though that this
is dummy example. With real-life project you would end up with a lot more of dependency
handling during bootstrap phase.

Now let's see how it looks like with injectme. Using the same project, we can improve on
the dependency management part like this:


.. code-block:: python
    :caption: Contents of src/users.py

    from injectme import inject


    class UsersRepository:
        def __init__(self, users):
            self.users = users

        def get_users(self):
            return self.users


    @inject
    class UsersService:
        users_repo: UsersRepository

        def show_users(self):
            print(self.users_repo.get_users())


.. code-block:: python
    :caption: Contents of src/cars.py

    from injectme import inject


    class CarsRepository:
        def __init__(self, cars):
            self.cars = cars

        def get_cars(self):
            return self.cars


    @inject
    class CarsService:
        cars_repo: CarsRepository

        def show_cars(self):
            print(self.cars_repo.get_cars())


.. code-block:: python
    :caption: Contents of src/bootstrap.py

    from injectme import register

    from .app import App
    from .cars import CarsRepository, CarsService
    from .users import UsersRepository, UsersService


    def bootstrap():
        register(CarsRepository, CarsRepository(("cara", "carb")))
        register(UsersRepository, UsersRepository(("usera", "userb")))

        # repositories are automatically injected
        cars_service = CarsService()
        users_service = UsersService()

        return App(
            cars_service=cars_service,
            users_service=users_service,
        )


Pay attention to the ``UsersService`` and ``CarsService`` classes. Both has been decorated with
``@inject`` decorator. It marks them as targets for "injection". The dependencies required by a class
decoreated with ``@inject`` are specified as annotations (``cars_repo: CarsRepository``). Each annotation will become an attribute
of class's instance.
