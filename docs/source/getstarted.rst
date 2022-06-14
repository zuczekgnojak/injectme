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
        ├── bootstrap.py
        ├── repositories.py
        └── services.py


.. code-block:: python
    :caption: Contents of src/repositories.py

    class UsersRepository:
        def __init__(self, users):
            self.users = users

        def get_users(self):
            return self.users


    class CarsRepository:
        def __init__(self, cars):
            self.cars = cars

        def get_cars(self):
            return self.cars


.. code-block:: python
    :caption: Contents of src/services.py

    from .repositories import (
        CarsRepository,
        UsersRepository,
    )


    class CarsService:
        def __init__(self, cars_repo: CarsRepository):
            self.cars_repo = cars_repo

        def show_cars(self):
            print(self.cars_repo.get_cars())


    class UsersService:
        def __init__(self, users_repo: UsersRepository):
            self.users_repo = users_repo

        def show_users(self):
            print(self.users_repo.get_users())


    class RentalService:
        def __init__(
            self,
            cars_repo: CarsRepository,
            users_repo: UsersRepository,
        ):
            self.cars_repo = cars_repo
            self.users_repo = users_repo

        def rent(self):
            print(self.cars_repo.get_cars())
            print(self.users_repo.get_users())


.. code-block:: python
    :caption: Contents of src/bootstrap.py

    from .repositories import CarsRepository, UsersRepository
    from .services import (
        CarsService,
        UsersService,
        RentalService,
    )

    cars_repository = CarsRepository(("cara", "carb"))
    users_repository = UsersRepository(("usera", "userb"))

    cars_service = CarsService(cars_repository)
    users_service = UsersService(users_repository)
    rental_service = RentalService(
        cars_repo=cars_repository,
        users_repo=users_repository,
    )


There is no much code in here so it does not look that bad. Be aware though that this
is dummy example. With real-life project you would end up with a lot more of dependency
handling during bootstrap phase.

Now let's see how it looks like with injectme. Using the same project, we can improve on
the dependency management part like this:


.. code-block:: python
    :caption: Contents of src/services.py

    from injectme import inject

    from .repositories import (
        CarsRepository,
        UsersRepository,
    )


    @inject
    class CarsService:
        cars_repo: CarsRepository

        def show_cars(self):
            print(self.cars_repo.get_cars())


    @inject
    class UsersService:
        users_repo: UsersRepository

        def show_users(self):
            print(self.users_repo.get_users())


    @inject
    class RentalService:
        cars_repo: CarsRepository
        users_repo: UsersRepository

        def rent(self):
            print(self.cars_repo.get_cars())
            print(self.users_repo.get_users())


.. code-block:: python
    :caption: Contents of src/bootstrap.py

    from injectme import register

    from .repositories import CarsRepository, UsersRepository
    from .services import (
        CarsService,
        UsersService,
        RentalService,
    )

    register(CarsRepository, CarsRepository(("cara", "carb")))
    register(UsersRepository, UsersRepository(("usera", "userb")))

    cars_service = CarsService()
    users_service = UsersService()
    rental_service = RentalService()


Pay attention to the ``*Service`` classes. All of them have been decorated with
``@inject`` decorator. It marks them as targets for "injection". The dependencies required by a class
decoreated with ``@inject`` are specified as annotations (e.g. ``cars_repo: CarsRepository``). Each annotation will become an attribute
of class's instance.

.. note::
    In the example with injectme there are no changes to the `src/repositories.py` file so it's not included. Don't get fooled by reduced
    amount of code.
