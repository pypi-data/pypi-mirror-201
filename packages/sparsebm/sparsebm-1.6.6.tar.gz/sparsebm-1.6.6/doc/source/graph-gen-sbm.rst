Graph generation with SBM
-------------------------

The function ``generate_SBM_dataset`` generates a graph using the Stochastic Block Model with a specified number of nodes, the number of clusters, the cluster proportions, and the array of connection probabilities between classes.
The argument *symmetric* indicates whether the adjacency matrix has to be symmetric.
The generated sparse adjacency matrix and the generated indicator matrix of the latent clusters are returned as an `SBM_dataset` object.
The graph generation is implemented such that the adjacency matrix :math:`X` is created block by block and never handles dense matrices.

.. autofunction:: sparsebm.generate_SBM_dataset

.. autoclass:: sparsebm._datatypes.SBM_dataset
