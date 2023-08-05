# pylint: skip-file

import numpy as np
import sparsebm
from sparsebm import generate_LBM_dataset, ModelSelection
from sparsebm.utils import reorder_rows, ARI, CARI
import scipy.sparse as ss
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument(
    "-r",
    "--repeat",
    type=int,
    help="Number of arrays for each dimension to be generated.",
    required=False,
    default=100,
)
args = vars(parser.parse_args())
nbtt = args["repeat"]

if not os.path.exists("./experiments/data"):
    os.makedirs("./experiments/data")
if not os.path.exists("./experiments/data/size_fixed"):
    os.makedirs("./experiments/data/size_fixed")


###
### Specifying the parameters of the dataset to generate.
###
number_of_rows = int(1 * 10**4)
number_of_columns = int(number_of_rows / 2)
nb_row_clusters, nb_column_clusters = 3, 4
row_cluster_proportions = (
    np.ones(nb_row_clusters) / nb_row_clusters
)  # Here equals classe sizes
column_cluster_proportions = (
    np.ones(nb_column_clusters) / nb_column_clusters
)  # Here equals classe sizes

e = 0.25
connection_probabilities = np.array(
    [[4 * e, e, e, e * 2], [e, e, e, e], [2 * e, e, 2 * e, 2 * e]]
)


###
### Generate The dataset.
###
import pickle

nbexpo = 7
for exponent in range(nbexpo):
    print("exponent {}/{}".format(exponent, nbexpo))
    for i in range(nbtt):
        print("Generate dataset {}/{}".format(i, nbtt))
        dataset = generate_LBM_dataset(
            number_of_rows,
            number_of_columns,
            nb_row_clusters,
            nb_column_clusters,
            connection_probabilities / 2**exponent,
            row_cluster_proportions,
            column_cluster_proportions,
            sparse=False,
        )
        dataset["data"] = ss.coo_matrix(dataset["data"])
        dataset["exponent"] = exponent
        fname = (
            str(number_of_rows)
            + "_"
            + str(number_of_columns)
            + "_"
            + str(exponent)
            + "_"
            + str(i)
            + ".pkl"
        )
        pickle.dump(dataset, open("./experiments/data/size_fixed/" + fname, "wb"))
