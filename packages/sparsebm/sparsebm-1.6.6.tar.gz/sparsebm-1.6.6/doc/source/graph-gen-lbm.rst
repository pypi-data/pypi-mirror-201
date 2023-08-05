Graph generation with LBM
-------------------------

The function ``generate_LBM_dataset`` generates a graph following the Latent Block Model with a specified number of nodes of each type, the number of clusters of each type, the cluster proportions, and the array of connection probabilities between classes. 
The generated sparse adjacency matrix and the generated latent cluster indicator matrix are returned as an `LBM_dataset` object.
The graph generation is implemented such that the adjacency matrix :math:`X` is created block by block and never handles dense matrices.

.. autofunction:: sparsebm.generate_LBM_dataset

.. autoclass:: sparsebm._datatypes.LBM_dataset
