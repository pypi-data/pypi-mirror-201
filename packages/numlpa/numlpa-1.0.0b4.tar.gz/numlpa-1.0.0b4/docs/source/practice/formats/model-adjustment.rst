Model adjustment data format
============================

A model adjustment is the result of an optimization process aimed at determining the value of the model parameters that minimizes the deviation of its prediction from the true diffraction profile.
The data related to a model adjustment is contained in a dictionnary whose structure is given below.

.. code-block:: python

   {
       'metadata': {
           'type': 'model-adjustment',
           'date': 'YYYY-MM-DDTHH:MM:SS+00:00',
           'version': version_tuple,
       },
       'distribution': {
           ...
       },
       'region': {
           ...
       },
       'diffraction': {
           ...
       },
       'profile': {
           'harmonic': harmonic,
           'part': 'real',
           'variable': [L0, L1, ...],
           'amplitude': [A_L0, A_L1, ...],
       },
       'limits': {
           'restriction': n_max_restriction,
           ...
       },
       'model': {
           'module': 'numlpa.kits.models.name',
           'variable': [L0, L1, ...],
           'amplitude': [A_L0, A_L1, ...],
       },
       'optimization': {
           'module': 'numlpa.kits.optimizers.name',
           'restriction': 'restriction',
           'rss': residual_sum_of_squares,
       },
       'parameters': {
           'names': ['parameter_1', 'parameter_2', ...],
           'values': [p1_optimal_value, p2_optimal_value, ...],
           'real': [p1_real_value, p2_real_value, ...]
           'relative': [p1_relative_value, p2_relative_value, ...],
       },
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

* ``diffraction``: Section containing data related to the diffraction proccess.

  * See :doc:`Fourier transform data format <fourier-transform>`.

* ``profile``: Section containing data related to the real diffraction profile.

  * ``harmonic``: Harmonic chosen for the fit.

  * ``part``: Part of the Fourier transform used for the fit.

  * ``variable``: Fourier transform variable values (in metre).

  * ``amplitude``: Amplitude true values.

* ``limits``: Section related to the different restrictions that could be applied.

  * All possible restrictions are given with their corresponding number of points.

* ``model``: Section related to the diffraction profile outputed by the adjusted model.

  * ``module``: Name of the LPA model implementation used.

  * ``variable``: Fourier transform variable values (in metre).

  * ``amplitude``: Adjusted amplitude values.

* ``optimization``: Section related to the optimization process.

  * ``module``: Name of the module used for optimizing.

  * ``restriction``: Name of the Fourier variable restriction used.

  * ``rss``: Value of the residual sum of squares.

* ``parameters``: Section related to the LPA model parameters.

  * ``names``: Name of the parameters of the LPA model.

  * ``values``: Optimal value of the parameters after adjustment.

  * ``real``: Real value of the parameters.

  * ``relative``: Optimal value divided by the real value for each parameter.
