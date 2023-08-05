
Model selection
---------------

The *ModelSelection* class encapsulates the model selection algorithm based on
the split and merge strategy. The argument *model_type* specifies the model to use
and *n_clusters_max* specifies an upper limit of the number of groups the algorithm can explore.
The split strategy stops when the number of classes is
greater than :math:`min(1.5 \cdot nnq\_best,\; nnq\_best + 10,\; n\_clusters\_max)`
with :math:`nnq\_best` being the number of classes of the best model found so far
during the split strategy.
The merge strategy stops when the minimum relevant number of classes is reached.
The split and merge strategy alternates until no best model is found for two iterations.

The argument *plot* specifies if an illustration is displayed to the user during the learning process.

.. autoclass:: sparsebm.ModelSelection
   :members:

   .. automethod:: __init__

.. autoclass:: sparsebm._datatypes.ModelSelectionResults
   :members:
