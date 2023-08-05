Configuration
=============

Using the command-line interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

What will be your best ally in configuring the features is the ``-h`` or ``--help`` option.
This option will show you what can be configured at each stage of the construction of a command.
Start by running the following command:

.. code-block:: bash

   stemplate -h

You will then see what you can put after "stemplate" in the command line.
Note that the command-line interface (CLI) uses nested subparsers and that the options for a given parser must be placed just after the parser name and before its potential subparsers.
For this reason, until you understand what is going on in the CLI, try to respect the order of the options.

In the previous page we showed how to display the date with the ``date`` subparser.
If you want to know what options are available for the date subparser, run the ``stemplate date -h`` command.
You will discover that there is a ``color`` option.
Then, you can change the default color and display the date in red with the following command:

.. code-block:: bash

   stemplate date --color red

Using a configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~~

Everything that can be configured via the CLI can also be configured from a configuration file.
The default configuration of the package is defined in the `default.conf <https://gitlab.com/stemplate/pypack/-/blob/main/src/stemplate/default.conf>`_ file.
The easiest way to create your own configuration file is to copy this file and modify its content.

Let's now assume that you have named your own configuration file ``custom.conf``.
To get the same result as before without specifying the color in the command line, change the value of the ``color`` entry in the ``stemplate.main.date`` section of the configuration file and run:

.. code-block:: bash

   stemplate --config custom.conf date

It is not necessary to keep all the sections in the configuration file.
You can delete all the sections and options you have not modified.
If you look at the structure of the package, you will notice that the names of the sections correspond to the names of the modules to which the options are attached.
