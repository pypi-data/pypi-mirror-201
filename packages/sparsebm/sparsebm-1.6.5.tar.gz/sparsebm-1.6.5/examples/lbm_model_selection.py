"""
=================================================================
A demo of the Model Selection applied to the Latent Block Model
=================================================================
This example demonstrates how to generate a dataset from the bernoulli LBM
and cluster it using the Latent Block Model without a prior knowledge on the
number of classes. The data is generated with the
``generate_LBM_dataset`` function, and passed to the ModelSelection
class. The rows and columns of the matrix are rearranged to show the clusters
found by the model.
"""

# pylint: disable=invalid-name

import numpy as np
import matplotlib.pyplot as plt

from sparsebm import generate_LBM_dataset, ModelSelection
from sparsebm.utils import reorder_rows, reorder_cols, ARI, CARI

print(__doc__)

###
### Specifying the parameters of the dataset to generate.
###
number_of_rows = 10**3
number_of_columns = number_of_rows // 2
nb_row_clusters, nb_column_clusters = 3, 4
row_cluster_proportions = (
    np.ones(nb_row_clusters) / nb_row_clusters
)  # Here equals classe sizes
column_cluster_proportions = (
    np.ones(nb_column_clusters) / nb_column_clusters
)  # Here equals classe sizes
connection_probabilities = (
    np.array(
        [
            [0.025, 0.0125, 0.0125, 0.05],
            [0.0125, 0.025, 0.0125, 0.05],
            [0, 0.0125, 0.025, 0],
        ]
    )
) * 2

assert (
    nb_row_clusters == connection_probabilities.shape[0]
    and nb_column_clusters == connection_probabilities.shape[1]
)

###
### Generate The dataset.
###
dataset = generate_LBM_dataset(
    number_of_rows,
    number_of_columns,
    nb_row_clusters,
    nb_column_clusters,
    connection_probabilities,
    row_cluster_proportions,
    column_cluster_proportions,
)

# instantiate the ModelSelection class.
lbm_model_selection = ModelSelection(
    model_type="LBM",  # Either 'LBM' or 'SBM', the model used to cluster the data.
    plot=True,  # display illustration of the model selection algorithm.
)

lbm_models = lbm_model_selection.fit(dataset.data)
lbm_selected = lbm_models.best

if lbm_selected.trained_successfully:
    print("Model has been trained successfully.")
    print(
        "Value of the Integrated Completed Loglikelihood is "
        f"{lbm_selected.get_ICL():.4f}"
    )
    print(f"The original number of row classes was {nb_row_clusters}")
    print(f"The model selection picked {lbm_selected.n_row_clusters} row classes")
    print(f"The original number of column classes was {nb_column_clusters}")
    print(f"The model selection picked {lbm_selected.n_column_clusters} column classes")
    row_ari = ARI(dataset.row_labels, lbm_selected.row_labels)
    column_ari = ARI(dataset.column_labels, lbm_selected.column_labels)
    co_ari = CARI(
        dataset.row_labels,
        dataset.column_labels,
        lbm_selected.row_labels,
        lbm_selected.column_labels,
    )
    print(f"Adjusted Rand index is {row_ari:.2f} for row classes")
    print(f"Adjusted Rand index is {column_ari:.2f} for column classes")
    print(f"Coclustering Adjusted Rand index is {co_ari:.2f}")
original_matrix = dataset.data.copy()
reorder_rows(original_matrix, np.argsort(dataset.row_labels))
reorder_cols(original_matrix, np.argsort(dataset.column_labels))

reconstructed_matrix = dataset.data.copy()
reorder_rows(reconstructed_matrix, np.argsort(lbm_selected.row_labels))
reorder_cols(reconstructed_matrix, np.argsort(lbm_selected.column_labels))

figure, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(8, 5), constrained_layout=True)
# Plotting the original matrix.
ax1.spy(dataset.data, markersize=0.05, marker="*", c="black")
ax1.set_title("Original data matrix")
ax1.axis("off")
# Plotting the original ordered matrix.
ax2.spy(original_matrix, markersize=0.05, marker="*", c="black")
ax2.set_title("Data matrix reordered \naccording to the \noriginal classes")
ax2.axis("off")
# Plotting the matrix reordered by the LBM.
ax3.spy(reconstructed_matrix, markersize=0.05, marker="*", c="black")
ax3.set_title("Data matrix reordered \naccording to the \nclasses given by the LBM")
ax3.axis("off")
plt.show()
