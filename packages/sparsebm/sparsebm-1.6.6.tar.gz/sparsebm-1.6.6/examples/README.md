# Examples

## Notebooks examples, GPU recommended

These examples simulate large networks, and perform estimations with known and
unknown number of groups. **It is highly recommended to have a GPU to run these
examples.** You can freely use [Google Colab] to run these notebooks with GPU.

- [sbm_in_colab.ipynb](sbm_in_colab.ipynb): Notebook with large symmetric network with SBM

- [lbm_in_colab.ipynb](lbm_in_colab.ipynb): Notebook with large bipartite network with LBM]

[Google Colab]: https://colab.research.google.com

## Scripts examples

These examples simulate small networks (around 1000 nodes), and perform
estimations.

### Symmetric networks with SBM:

- [sbm_random_init.py](sbm_random_init.py): Estimation with a known number of groups.

- [sbm_model_selection.py](sbm_model_selection.py): Estimation with a unknown number of groups (model selection).

### Bipartite networks with LBM:

- [lbm_random_init.py](lbm_random_init.py): Estimation with a known numbers of groups.

- [lbm_model_selection.py](lbm_model_selection.py): Estimation with a unknown numbers of groups (model selection).
