Fourier transform data format
=============================

A Fourier transform is the result of the Fourier analysis after diffraction.
The data related to a Fourier transform is contained in a dictionnary whose structure is given below.

.. code-block:: python

   {
       'metadata': {
           'type': 'fourier-transform',
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
           'module': 'numlpa.kits.diffractometers.name',
           'z_uvw': [u, v, w],
           'x_uvw': [u, v, w],
           'b_uvw': [u, v, w],
           'g_hkl': [h, k, l],
           'type': 'dislocation-type',
           'cell': cell,
           'step': step,
           'poisson': poisson,
           'contrast': contrast,
           'samples': samples,
           'replicate': replicate,
           'duration': duration,
           'points': points,
           ...
       },
       'coefficients': {
           'harmonic': [h0, h1, ...],
           'variable': [L0, L1, ...],
           'cos_mean': [
               [avg_cos_L0_h0, avg_cos_L1_h0, ...],
               [avg_cos_L0_h1, avg_cos_L1_h1, ...],
               ...
           ],
           'sin_mean': [
               [avg_sin_L0_h0, avg_sin_L1_h0, ...],
               [avg_sin_L0_h1, avg_sin_L1_h1, ...],
               ...
           ],
           'cos_deviation': [
               [std_cos_L0_h0, std_cos_L1_h0, ...],
               [std_cos_L0_h1, std_cos_L1_h1, ...],
               ...
           ],
           'sin_deviation': [
               [std_sin_L0_h0, std_sin_L1_h0, ...],
               [std_sin_L0_h1, std_sin_L1_h1, ...],
               ...
           ],
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

  * ``module``: Name of the module used for the diffraction.

  * ``z_uvw``: Direction of the line vector (uvw).

  * ``x_uvw``: Direction of the Fourier variable (uvw).

  * ``b_uvw``: Direction of the Burgers vector (uvw).

  * ``g_hkl``: Direction of the diffraction vector (hkl).

  * ``type``: Dislocation type (``'screw'`` or ``'edge'``).

  * ``cell``: Lattice constant (in metre).

  * ``step``: Step size of the Fourier variable (in metre).

  * ``poisson``: Poisson number.

  * ``contrast``: Contrast factor.

  * ``samples``: Number of dislocation samples used.

  * ``replicate``: Number of replication of the region of interest.

  * ``duration``: Calculation time (in second).

  * ``points``: Number of random points for the Monte Carlo method.

* ``coefficients``: Section containing data related to the Fourier coefficients.

  * ``harmonic``: List of Fourier harmonics.

  * ``variable``: List of Fourier variables (in metre).

  * ``cos_mean``: Cosine coefficients for each harmonic and Fourier variable.

  * ``sin_mean``: Sine coefficients for each harmonic and Fourier variable.

  * ``cos_deviation``: Cosine coefficients standard deviation for each harmonic and Fourier variable.

  * ``sin_deviation``: Sine coefficients standard deviation for each harmonic and Fourier variable.
