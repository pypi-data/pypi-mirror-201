Editable installation
=====================

.. note::

   If you have not already done so, please install `Git <https://git-scm.com>`_ on your computer.

To work on the package source files and quickly test the changes, you can install the package in `development mode <https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#working-in-development-mode>`_.
To do this, clone the project from its `GitLab repository <https://gitlab.com/x-rays/numlpa>`_ with the command below.

.. code-block:: bash

   git clone https://gitlab.com/x-rays/numlpa.git

The shell script `setup.sh <https://gitlab.com/x-rays/numlpa/-/blob/main/setup.sh>`_ has been specially created to automate all remaining operations for the installation in development mode.
This script will automatically install and activate a virtual environment containing all the necessary dependencies for the development and operation of the package.
Each time you want to work on the package you will just have to go to the project directory and run the command below:

.. code-block:: bash

   source setup.sh

You can also install the package in development mode with the command ``pip install -e .`` in the environment of your choice.
But the advantage of the ``setup.sh`` is that it manages the virtual environment and automatically installs the packages used to generate the documentation and lint the code.
More information is provided in the ``setup.sh`` file.
