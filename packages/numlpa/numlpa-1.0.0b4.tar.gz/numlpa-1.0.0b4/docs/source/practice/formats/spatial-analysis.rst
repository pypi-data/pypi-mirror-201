Spatial analysis data format
=============================

A spatial analysis is the result of a calculation carried out on each pair of dislocations to determine the interaction term and the distribution of dislocations around a dislocation.
The data related to a spatial analysis is contained in a dictionnary whose structure is given below.

.. code-block:: python

   {
       'metadata': {
           'type': 'spatial-analysis',
           'date': 'YYYY-MM-DDTHH:MM:SS+00:00',
           'version': version_tuple,
       },
       'distribution': {
           ...
       },
       'region': {
           ...
       },
       'analysis': {
           'module': 'numlpa.kits.analyzers.name',
           'type': 'dislocation-type',
           'r_0': r_0,
           'r_roi': r_roi,
           'r_max': r_max,
           'steps': steps,
           'poisson': poisson,
           'shear': shear,
           'r_cut': r_cut,
           'self_energy': self_energy,
           'interaction_energy': interaction_energy,
           'total_energy': total_energy,
           'variable': [r0, r1, r2, ...],
           'count_mm': [n_mm_0, n_mm_1, n_mm_2, ...],
           'count_mp': [n_mp_0, n_mp_1, n_mp_2, ...],
           'count_pm': [n_pm_0, n_pm_1, n_pm_2, ...],
           'count_pp': [n_pp_0, n_pp_1, n_pp_2, ...],
           'samples': samples,
           'duration': duration,
       }
   }

Description of mandatory entries:

* ``metadata``: Section containing general information related to the nature of the data.

  * ``type``: Identifier associated with the data category.

  * ``date``: Date of data generation, in `ISO 8601 <https://www.iso.org/iso-8601-date-and-time-format.html>`_ standard.

  * ``version``: Version of NumLPA.

* ``distribution``: Section containing data related to the dislocation probability distribution.

  * See :doc:`dislocation sample data format <dislocation-sample>`.

* ``region``: Section containing data related to the region of interest.

  * See :doc:`dislocation sample data format <dislocation-sample>`.

* ``analysis``: Section containing data related to the spatial analysis.

  * ``module``: Name of the module used for the analysis.

  * ``type``: Dislocation type (``'screw'`` or ``'edge'``).

  * ``r_0``: Core radius (in metre).

  * ``r_roi``: Size of the region of interest (in metre).

  * ``r_max``: Maximum radius value (in metre).

  * ``steps``: Number of subdivision on the absice axis.

  * ``poisson``: Poisson number.

  * ``shear``: Shear modulus (in pascal).

  * ``r_cut``: Outer cut-off radius (in metre).

  * ``self_energy``: Self energy per unit length (in joule per metre).

  * ``interaction_energy``: Interaction energy per unit length (in joule per metre).

  * ``total_energy``: Total energy per unit length (in joule per metre).

  * ``variable``: Boundary radius of the cylinder shells for the counting of dislocations (in metre).

  * ``count_mm``: Number of dislocations ``-`` around a dislocation ``-`` in each cylinder shell.

  * ``count_mp``: Number of dislocations ``+`` around a dislocation ``-`` in each cylinder shell.

  * ``count_pm``: Number of dislocations ``-`` around a dislocation ``+`` in each cylinder shell.

  * ``count_pp``: Number of dislocations ``+`` around a dislocation ``+`` in each cylinder shell.

  * ``samples``: Number of dislocation samples used.

  * ``duration``: Calculation time (in second).
