Use virtual environments
========================

.. note::

   This step **is not necessary** for the installation of the package.
   You can skip it.
   **But** if you don't know about virtual environments you may lose the opportunity to keep the Python packages you install on your computer tidy.

Why?
----

What is presented here allows you to install the package in an isolated space so that it does not interfere with the rest of the packages you have installed on your computer.
This offers several advantages:

* **Work on several projects with different packages**

  * You can create different virtual environments for different projects each requiring different packages or package versions.

  * You can delete all traces of the packages installed for a project by deleting the virtual environment associated to the project.

  * You can use a virtual environment to modify the code of a package and another virtual environment to keep an official release of the package.

* **Start a project from a clean environment**

  * When you create a virtual environment, only the pip and setuptools packages are preinstalled.

  * Then you will have to install the packages you need in this new (and almost empty) environment.

  * This way, you can easily establish the list of necessary and sufficient packages for the operation of your project.

* **Facilitate the recreation of a work environment**

  * You can list the packages required for a project and their version in a ``requirements.txt`` file.

  * This way, for another person, another machine, or another location on your computer, it will be easy to recreate the conditions of functioning of your project by initiating a virtual environment and executing the command ``pip install -r requirements.txt``.

If you want more information, you can consult the `Python venv package documentation <https://docs.python.org/3/library/venv.html>`_.

How?
----

It is very simple.
There are only four steps and nothing to install.

Create your virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This step is to be performed once for each new project.
Choose a path for your virtual environment and execute the following command:

.. code-block:: bash

   python3 -m venv location-of-your-choice

Activate your virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This step is to be performed every time you open a terminal to work on a project.
In the previous step, the virtual environment was created.
But to "work in it" you have to run:

.. code-block:: bash

   . location-of-your-choice/bin/activate

When this command is executed, your terminal "enters" the virtual environment.
The python packages that you install will now be placed in the virtual environment.
When used from within a virtual environment, common installation tools such as pip will install Python packages into the virtual environment without needing to be told to do so explicitly.

Deactivate your virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This step is to be performed when you want to leave the virtual environment or before activating another one.
To leave your virtual environment, run:

.. code-block:: bash

   deactivate

Closing your terminal also does the trick.
Note that this does not delete the virtual environment.
You will be able to find everything you have installed by reactivating your virtual environment.

Delete your virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you are done with a project, or you want to move your virtual environment, you can delete it with the command :

.. code-block:: bash

   rm -r location-of-your-choice

And now?
--------

It is advisable to execute the installation command presented on the following page from a virtual environment that you have created and activated as shown above.
