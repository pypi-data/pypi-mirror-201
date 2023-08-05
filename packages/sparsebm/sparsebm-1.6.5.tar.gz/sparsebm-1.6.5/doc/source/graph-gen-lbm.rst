Graph generation with LBM
-------------------------

The function *generate_LBM_dataset* generates a graph using the LBM with a specified numbers of nodes of each type, numbers of clusters of each type, the cluster proportions, and the array of connection probabilities between classes.
The generated sparse adjacency matrix and the generated indicator matrix of the latent clusters are returned a `LBM_dataset` object.
The graph generation is implemented such as the adjacency matrix X is created block after block and never manipulates dense matrices.


.. autofunction:: sparsebm.generate_LBM_dataset

.. autoclass:: sparsebm._datatypes.LBM_dataset
