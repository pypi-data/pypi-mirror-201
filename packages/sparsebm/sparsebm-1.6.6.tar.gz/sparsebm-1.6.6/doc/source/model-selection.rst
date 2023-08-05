
Model selection
---------------

The `ModelSelection` class encapsulates the model selection algorithm based on the
split and merge strategy. The *model_type* argument specifies the model to use
and *n_clusters_max* specifies the upper limit of the number of clusters the algorithm explores.
The splitting strategy stops when the number of classes is
greater than :math:`min(1.5 \cdot nnq\_best,\ ; nnq\_best + 10,\ ; n\c_clusters\max)`
where :math:`nq\_best` is the number of classes of the best model found so far.
The merge strategy stops when the minimum number of classes is reached.
The split and merge strategies alternate until no improvement over two iterations.

The *plot* argument indicates whether an illustration is displayed to the user during the learning process.

.. autoclass:: sparsebm.ModelSelection
   :members:

   .. automethod:: __init__

.. autoclass:: sparsebm._datatypes.ModelSelectionResults
   :members:
