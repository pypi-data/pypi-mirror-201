Dislocation sample data format
==============================

A dislocation sample is an outcome of a random draw from a probability distribution in a given region of space.
The data related to a dislocation sample is contained in a dictionnary whose structure is given below.

.. code-block:: python

   {
       'metadata': {
           'type': 'dislocation-sample',
           'date': 'YYYY-MM-DDTHH:MM:SS+00:00',
           'version': version_tuple,
       },
       'distribution': {
           'module': 'numlpa.kits.distributions.name',
           'seed': seed,
           'density': density,
           ...
       },
       'region': {
           'type': 'shape-identifier',
           ...
       },
       'dislocations': {
           'senses': [s0, s1, ...],
           'positions': [
               [x0, x1, ...],
               [y0, y1, ...],
           ],
       },
   }

Description of mandatory entries:

* ``metadata``: Section containing general information related to the nature of the data.

  * ``type``: Identifier associated with the data category.

  * ``date``: Date of data generation, in `ISO 8601 <https://www.iso.org/iso-8601-date-and-time-format.html>`_ standard.

  * ``version``: Version of NumLPA.

* ``distribution``: Section containing data related to the dislocation probability distribution.

  * ``module``: Name of the module used for generation.

  * ``seed``: Integer serving as a random seed.

  * ``density``: Exact density of the distribution (dislocations per square metre).

* ``region``: Section containing data related to the region of interest.

  * ``type``: Identifier associated with the spatial delimitation category.

* ``dislocations``: Section containing data related to the generated dislocations.

  * ``senses``: Sense of the Burgers vector of each dislocation (-1 or 1).

  * ``positions``: Spatial coordinates of each dislocation (in metre).
