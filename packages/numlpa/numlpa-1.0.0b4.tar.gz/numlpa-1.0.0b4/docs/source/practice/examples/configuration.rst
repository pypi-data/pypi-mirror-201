Configuration
=============

Using the command-line interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

What will be your best ally in configuring the features is the ``-h`` or ``--help`` option.
This option will show you what can be configured at each stage of the construction of a command.
Start by running the following command:

.. code-block:: bash

   numlpa -h

You will then see what you can put after "numlpa" in the command line.
Note that the command-line interface (CLI) uses nested subparsers and that the options for a given parser must be placed just after the parser name and before its potential subparsers.
For this reason, until you understand what is going on in the CLI, try to respect the order of the options.
