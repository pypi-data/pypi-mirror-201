# Experiments

## Analyzing the benefit of the inference optimized for sparse graphs.

Our optimized inference for sparse graphs is compared to standard inference in terms of computational cost.
The experiments are conducted here on the latent block model, but similar results can be obtained for the stochastic block model.

### Fixed edge sparsity rate, varying network size

:warning: **This experiment must be run on a GPU. Use google colab if needed.**


1. Generate the datasets with
```
python experiments/sparse_sparsity_fixed_generate_data.py
```
If you want to experiment on more or less repetitions use argument repeat:
```
python experiments/sparse_sparsity_fixed_generate_data.py --repeat 1
```

2. The LBM is trained on each data matrix using the inference optimized for sparse graph and the original one.
To launch the inference use:
```
python experiments/sparse_sparsity_fixed.py
```

3. To plot the results, use:
```
python experiments/sparse_sparsity_fixed_results.py
```

### Fixed network size, varying edge sparsity rate

This experiment shows that the SparseBM implementation preserves the GPU memory and is faster when there are few edges.

:warning: This experiment **must** be run with a **GPU with at least 20GB** of memory.

1. Generate the datasets with
```
python experiments/sparse_size_fixed_generate_data.py
```
If you want to experiment on more or less repetitions use argument repeat:
```
python experiments/sparse_size_fixed_generate_data.py --repeat 1
```

2. The LBM is trained on each data matrix using standard inference and the one optimized for sparse graphs.
To launch the inference use:
```
python experiments/sparse_size_fixed.py
```

3. To plot the results, use:
```
python experiments/sparse_size_fixed_results.py
```

## Comparing SparseBM with existing R packages.

1. The SparseBM implementation of the LBM  is compared to those available in the Blockcluster and Blockmodels packages.
The data set generated in the previous experiment with varying network size and fixed sparsity rate is re-used. If the dataset has not been generated yet, use:
```
python experiments/sparse_sparsity_fixed_generate_data.py
```
If you want to experiment on more or less repetitions use argument repeat:
```
python experiments/sparse_sparsity_fixed_generate_data.py --repeat 1
```

2. :warning: To execute this experiment, [R must be installed](https://cran.r-project.org/bin/linux/ubuntu/README.html) as well as the [blockcluster](https://cran.r-project.org/web/packages/blockcluster/index.html) and [blockmodels](https://cran.r-project.org/web/packages/blockmodels/index.html) packages.
To bind R packages with Python, the rpy2 module must be installed with
```
pip install rpy2
```

3. To launch the benchmark with all algorithms, use:
```
python experiments/benchmark_libraries.py
```
To avoid memory problems, the programs gets the system memory and adapts, for each algorithm, the maximum size of the matrix to process.
To override this default behavior, you can specify the maximum size and the algorithm you want to use:
```
python experiments/benchmark_libraries.py --programs sparsebm --size=80000
```
In this example, the benchmark is run only with SparseBM and on all matrices of maximum size 80000 times 40000.

4. To plot the results, use:
```
python experiments/benchmark_libraries_results.py
```
