Graph generation with SBM
-------------------------

The function *generate_SBM_dataset* generates a graph using the SBM with a specified number of nodes, a number of clusters, the cluster proportions, and the array of connection probabilities between classes.
The argument *symmetric* indicates if the adjacency matrix has to be symmetric.
The generated sparse adjacency matrix and the generated indicator matrix of the latent clusters are returned a `SBM_dataset` object.
The graph generation is implemented such as the adjacency matrix X is created block after block and never manipulates dense matrices.

.. autofunction:: sparsebm.generate_SBM_dataset

.. autoclass:: sparsebm._datatypes.SBM_dataset
