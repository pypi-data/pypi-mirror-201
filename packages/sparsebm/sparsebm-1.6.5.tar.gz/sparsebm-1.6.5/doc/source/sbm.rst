Stochastic Block Model
----------------------
.. image:: sbm.png
        :scale: 50
        :align: center
        :alt: sbm

The SBM is encapsulated in the *SBM* class that inherits from the
**sklearn.base.BaseEstimator** that is the base class for all estimators
in scikit-learn.
A number of clusters should be specify with the parameter *n_clusters* otherwise
the default value 5 is used.
If the **cupy** module is installed, the class is using the GPU with higher
memory available. The parameter *use_gpu* can disable this behaviour and the parameter *gpu_index* can enforce the use of a specific GPU.

The class implements the random initializations strategy that corresponds to the run of *n_iter_early_stop* EM steps on *n_init* random initializations,
followed by iterations until convergence of the criterion for the *n_init_total_run* best results after these preliminary steps;
*n_iter_early_stop*, *n_init* and *n_init_total_run* being parameters of the class.

The convergence of the criterion :math:`J(q_\gamma, \theta)` is declared when

.. math::
    J^{(t)}(q_\gamma, \theta) - J^{(t-5)}(q_\gamma, \theta) \leq ( atol + rtol \cdot \lvert J^{(t)}(q_\gamma, \theta)\rvert),

with *atol* and *rtol* being respectively the absolute tolerance and the relative tolerance.

.. autoclass:: sparsebm.SBM
   :members:

   .. automethod:: __init__
