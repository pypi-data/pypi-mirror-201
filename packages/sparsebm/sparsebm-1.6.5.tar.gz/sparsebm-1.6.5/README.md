# Getting started with SparseBM

SparseBM is a python module for handling sparse graphs with Block Models.
The module is an implementation of the variational inference algorithm for the Stochastic Block Model (SBM) and the Latent Block Model (LBM) for sparse graphs, which leverages the sparsity of edges to scale to very large numbers of nodes. The module can use [Cupy] to take advantage of the hardware acceleration provided by graphics processing units (GPU).

## Installing

The SparseBM module is distributed through the [PyPI repository](https://pypi.org/project/sparsebm/) and the documentation is available [here](https://jbleger.gitlab.io/sparsebm).


### With GPU acceleration (recommended if GPUs are available)

This option is recommended if GPUs are available to speedup computation.

With the package installer pip:

```
pip3 install sparsebm[gpu]
```

The [Cupy] module will be installed as a dependency.

[Cupy]: https://cupy.dev/

Alternatively [Cupy] can be installed separately, and will be used by `sparsebm`
if available.

```
pip3 install sparsebm
pip3 install cupy
```

### Without GPU acceleration

Without GPU acceleration, only CPUs are used. The infererence process still uses
sparsity, but no GPU linear algebra operations.

```
pip3 install sparsebm
```

For users who do not have GPU, we recommend the free serverless Jupyter notebook
environment provided by [Google Colab] where the Cupy module is already
installed and ready to be used with a GPU.

Complete examples (notebook for [Google Colab] and scripts) are given in the
Examples section (and in the `examples/` of the repository).

[Google Colab]: https://colab.research.google.com/

## Quick example with the Stochastic Block Model

- Generate a synthetic graph for analysis with SBM:

    ```python
    from sparsebm import generate_SBM_dataset

    dataset = generate_SBM_dataset(symmetric=True)
    ```


- Infer with the Bernoulli Stochastic Bloc Model:

    ```python
    from sparsebm import SBM

    # A number of classes must be specified. Otherwise see model selection.
    model = SBM(dataset.clusters)
    model.fit(dataset.data, symmetric=True)
    print("Labels:", model.labels)
    ```

- Compute performance:

    ```python
    from sparsebm.utils import ARI
    ari = ARI(dataset.labels, model.labels)
    print("Adjusted Rand index is {:.2f}".format(ari))
    ```

- Model selection: Infer with the Bernoulli Stochastic Bloc Model with a unknown number of groups:
    ```python
    from sparsebm import ModelSelection

    model_selection = ModelSelection("SBM")
    models = model_selection.fit(dataset.data, symmetric=True)
    print("Labels:", models.best.labels)

    from sparsebm.utils import ARI
    ari = ARI(dataset.labels, models.best.labels)
    print("Adjusted Rand index is {:.2f}".format(ari))
    ```

## Quick example with the Latent Block Model

- Generate a synthetic graph for analysis with LBM:

    ```python
    from sparsebm import generate_LBM_dataset

    dataset = generate_LBM_dataset()
    ```

 - Use the Bernoulli Latent Bloc Model:

    ```python
    from sparsebm import LBM

    # A number of classes must be specified. Otherwise see model selection.
    model = LBM(
        dataset.row_clusters,
        dataset.column_clusters,
        n_init_total_run=1,
    )
    model.fit(dataset.data)
    print("Row Labels:", model.row_labels)
    print("Column Labels:", model.column_labels)
    ```

- Compute performance:

    ```python
    from sparsebm.utils import CARI
    cari = CARI(
        dataset.row_labels,
        dataset.column_labels,
        model.row_labels,
        model.column_labels,
    )
    print("Co-Adjusted Rand index is {:.2f}".format(cari))
    ```

- Model selection: Infer with the Bernoulli Latent Bloc Model with a unknown number of groups:
    ```python
    from sparsebm import ModelSelection

    model_selection = ModelSelection("LBM")
    models = model_selection.fit(dataset.data)
    print("Row Labels:", models.best.row_labels)
    print("Column Labels:", models.best.column_labels)

    from sparsebm.utils import CARI
    cari = CARI(
        dataset.row_labels,
        dataset.column_labels,
        models.best.row_labels,
        models.best.column_labels,
    )
    print("Co-Adjusted Rand index is {:.2f}".format(cari))
    ```
