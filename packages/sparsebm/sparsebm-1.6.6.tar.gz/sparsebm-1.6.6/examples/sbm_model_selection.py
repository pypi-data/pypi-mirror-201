"""
=====================================================================
A demo of the Model Selection applied to the Stochastic Block Model
=====================================================================
This example demonstrates how to generate a dataset from the bernoulli SBM
and cluster it using the Stochastic Block Model without a prior knowledge on
the number of classes. The data is generated with the
``generate_SBM_dataset`` function, and passed to the ModelSelection
class. The rows and columns of the matrix are rearranged to show the clusters
found by the model.
"""

# pylint: disable=invalid-name

import numpy as np
import matplotlib.pyplot as plt

from sparsebm import generate_SBM_dataset, ModelSelection
from sparsebm.utils import reorder_rows_and_cols, ARI

print(__doc__)

# Specifying the parameters of the dataset to generate.
number_of_nodes = 10**3
number_of_clusters = 4
cluster_proportions = (
    np.ones(number_of_clusters) / number_of_clusters
)  # Here equals classe sizes
connection_probabilities = np.array(
    [
        [0.05, 0.018, 0.006, 0.0307],
        [0.018, 0.037, 0, 0],
        [0.006, 0, 0.055, 0.012],
        [0.0307, 0, 0.012, 0.043],
    ]
)  # The probability of link between the classes. Here symmetric.
assert (
    number_of_clusters
    == connection_probabilities.shape[0]
    == connection_probabilities.shape[1]
)


# Generate The dataset.
dataset = generate_SBM_dataset(
    number_of_nodes,
    number_of_clusters,
    connection_probabilities,
    cluster_proportions,
    symmetric=True,
)

# instantiate the ModelSelection class.
sbm_model_selection = ModelSelection(
    model_type="SBM",  # Either 'LBM' or 'SBM', the model used to cluster the data.
    plot=True,  # display illustration of the model selection algorithm.
)

sbm_models = sbm_model_selection.fit(dataset.data, symmetric=True)
sbm_selected = sbm_models.best

if sbm_selected.trained_successfully:
    print("Model has been trained successfully.")
    print(
        "Value of the Integrated Completed Loglikelihood is "
        f"{sbm_selected.get_ICL():.4f}"
    )
    print(f"The original number of classes was {number_of_clusters}")
    print(f"The model selection picked {sbm_selected.n_clusters} classes")
    ari = ARI(dataset.labels, sbm_selected.labels)
    print(f"Adjusted Rand index is {ari:.2f}")
#
original_matrix = dataset.data.copy()
reorder_rows_and_cols(original_matrix, np.argsort(dataset.labels))

reconstructed_matrix = dataset.data.copy()
reorder_rows_and_cols(reconstructed_matrix, np.argsort(sbm_selected.labels))

figure, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(8, 5), constrained_layout=True)
# Plotting the original matrix.
ax1.spy(dataset.data, markersize=0.05, marker="*", c="black")
ax1.set_title("Original data matrix")
ax1.axis("off")
# Plotting the original ordered matrix.
ax2.spy(original_matrix, markersize=0.05, marker="*", c="black")
ax2.set_title("Data matrix reordered \naccording to the\noriginal classes")
ax2.axis("off")
# Plotting the matrix reordered by the SBM.
ax3.spy(reconstructed_matrix, markersize=0.05, marker="*", c="black")
ax3.set_title("Data matrix reordered \naccording to the\nclasses given by the SBM")
ax3.axis("off")
plt.show()
