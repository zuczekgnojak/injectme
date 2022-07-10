Welcome to injectme's documentation!
====================================

injectme helps you use dependency injection effectively. It's simple
yet powerful and written entirely in python with no external dependencies.

Quick Example
~~~~~~~~~~~~~

.. code-block:: python
   :caption: Contents of example.py

   from injectme import inject, register

   class FileStorage:
       def save_file(self, path, data):
           print(f"Saving {path}")


   @inject
   class PicturesService:
       file_storage: FileStorage

       def save_picture(self, name, picture):
           self.file_storage.save_file(
               f"pictures/{name}", picture
           )


   register(FileStorage, FileStorage())

   pictures_service = PicturesService()
   pictures_service.save_picture("my-picture.jpg", b"...")


.. code-block:: shell

   $ python3 example.py

   Saving pictures/my-picture.jpg


.. note::
    This documentation is work in progress.


.. toctree::
   :caption: Injectme
   :maxdepth: 1
   :hidden:

   getstarted
   api


.. toctree::
   :caption: Guides
   :maxdepth: 1
   :hidden:

   guides/factories
   guides/injecting
