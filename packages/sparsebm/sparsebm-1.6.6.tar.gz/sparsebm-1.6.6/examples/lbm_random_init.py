"""
=============================================
A demo of the Latent Block Model
=============================================
This example demonstrates how to generate a dataset from the bernoulli LBM
and cluster it using the Latent Block Model.
The data is generated with the ``generate_LBM_dataset`` function,
and passed to the Latent Block Model. The rows and columns of the matrix
are rearranged to show the clusters found by the model.
"""

# pylint: disable=invalid-name

import numpy as np
import matplotlib.pyplot as plt

from sparsebm import generate_LBM_dataset, LBM
from sparsebm.utils import reorder_rows, reorder_cols, ARI, CARI

print(__doc__)

###
### Specifying the parameters of the dataset to generate.
###
number_of_rows = 2 * 10**3
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

# instantiate the Latent Block Model class.
model = LBM(
    nb_row_clusters,  # Number of row classes must be specify. Otherwise see model selection.
    nb_column_clusters,  # Number of column classes must be specify. Otherwise see model selection.
    n_init=100,  # Specifying the number of initializations to perform.
    n_iter_early_stop=10,  # Specifying the number of EM-steps to perform on each init.
    n_init_total_run=5,  # Specifying the number inits to keep and to train until convergence.
    verbosity=1,  # Either 0, 1 or 2. Higher value display more information to the user.
)
model.fit(dataset.data)

if model.trained_successfully:
    print("Model has been trained successfully.")
    print(f"Value of the Integrated Completed Loglikelihood is {model.get_ICL():.4f}")
    row_ari = ARI(dataset.row_labels, model.row_labels)
    column_ari = ARI(dataset.column_labels, model.column_labels)
    co_ari = CARI(
        dataset.row_labels,
        dataset.column_labels,
        model.row_labels,
        model.column_labels,
    )
    print(f"Adjusted Rand index is {row_ari:.2f} for row classes")
    print(f"Adjusted Rand index is {column_ari:.2f} for column classes")
    print(f"Coclustering Adjusted Rand index is {co_ari:.2f}")


original_matrix = dataset.data.copy()
reorder_rows(original_matrix, np.argsort(dataset.row_labels))
reorder_cols(original_matrix, np.argsort(dataset.column_labels))

reconstructed_matrix = dataset.data.copy()
reorder_rows(reconstructed_matrix, np.argsort(model.row_labels))
reorder_cols(reconstructed_matrix, np.argsort(model.column_labels))

figure, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(8, 5), constrained_layout=True)
# Plotting the original matrix.
ax1.spy(dataset.data, markersize=0.05, marker="*", c="black")
ax1.set_title("Original data matrix\n\n")
ax1.axis("off")
# Plotting the original ordered matrix.
ax2.spy(original_matrix, markersize=0.05, marker="*", c="black")
ax2.set_title("Data matrix reordered \naccording to the\n original classes")
ax2.axis("off")
# Plotting the matrix reordered by the LBM.
ax3.spy(reconstructed_matrix, markersize=0.05, marker="*", c="black")
ax3.set_title("Data matrix reordered \naccording to the\n classes given by the LBM")
ax3.axis("off")
plt.show()
