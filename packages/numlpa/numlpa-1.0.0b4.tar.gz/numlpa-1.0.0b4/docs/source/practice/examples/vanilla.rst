Vanilla example
===============

NumLPA contains a default configuration of almost all parameters.
You will see later how to use the command-line interface or your own configuration file to replace the default values.
For now, and thanks to all the preconfigured parameters, you will be able to test the package features with a minimum of effort.

Go to a blank working directory and run the following commands in a terminal:

.. code-block:: bash

   # generate dislocation samples
   numlpa draw samples.tar

   # compute Fourier transforms
   numlpa diffract samples.tar transforms.tar

   # merge Fourier transforms
   numlpa merge transforms.tar transform.tar

   # fit a model
   numlpa fit transform.tar adjustments.tar

   # generate figures
   numlpa export samples.tar fig-samples
   numlpa export transforms.tar fig-transforms
   numlpa export transform.tar fig-transform
   numlpa export adjustments.tar fig-adjustments

   # show the density accuracy of the model
   numlpa extract adjustments.tar -e parameters.relative.0 --mean

Here the figures are sent directly to folders for easy viewing, and the raw data are sent to tarballs.
But all input/output file containers can take the form of a zip file, a tarball or a folder.
The choice is yours.
Just remove the `.tar`, or replace it with a `.zip`, if you want to store the files in a different kind of container.
