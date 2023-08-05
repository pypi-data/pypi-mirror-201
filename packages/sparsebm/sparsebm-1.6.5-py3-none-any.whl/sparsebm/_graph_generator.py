# Copyright 2020-2023, Université de technologie de Compiègne, France,
#                      Gabriel Frisch <gabriel.frisch@hds.utc.fr>
# Copyright 2022-2023, Université de technologie de Compiègne, France,
#                      Jean-Benoist Leger <jbleger@hds.utc.fr>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# pylint: disable=missing-module-docstring

import logging
from typing import Optional

import numpy as np
import progressbar
import scipy.sparse

from sparsebm._datatypes import SBM_dataset, LBM_dataset

logger = logging.getLogger(__name__)


def generate_LBM_dataset(  # pylint: disable=too-many-locals,too-many-branches,too-many-arguments,invalid-name
    # pylint: disable=unsubscriptable-object
    number_of_rows: Optional[int] = None,
    number_of_columns: Optional[int] = None,
    nb_row_clusters: Optional[int] = None,
    nb_column_clusters: Optional[int] = None,
    connection_probabilities: Optional[np.ndarray] = None,
    row_cluster_proportions: Optional[np.ndarray] = None,
    column_cluster_proportions: Optional[np.ndarray] = None,
    verbosity: Optional[int] = 1,
    sparse: Optional[bool] = 1,
) -> dict:
    """Generate a sparse bipartite graph with Latent Block Models.

    Parameters
    ----------
    number_of_rows : int, optional, default : 2000
        The number of nodes of type (1).
    number_of_columns : int, optional, default : 1000
        The number of nodes of type (2).
    nb_row_clusters : int, optional, default : random between 3 and 5
        The number of classes of nodes of type (1).
    nb_column_clusters : int, default : random between 3 and 5
        The number of classes of nodes of type (2).
    connection_probabilities : np.ndarray, optional, default : random such as sparsity is 0.02
        The probability of having an edge between the classes.
    row_cluster_proportions : np.ndarray, optional, default : balanced
        Proportion of the classes of nodes of type (1).
    column_cluster_proportions : np.ndarray, optional, default : balanced
        Proportion of the classes of nodes of type (2).
    verbosity : int, optional, default : 1
        Display information during the generation process.
    sparse : bool, optional, default : True
        Use the classical matrix generation and not the sparse one.

    Returns
    -------
    LBM_dataset
        The generated dataset.

    Examples
    --------
    >>> generate_LBM_dataset()

    >>> connection_probabilities = (
    ...     np.array(
    ...         [
    ...             [0.025, 0.0125, 0.0125, 0.05],
    ...             [0.0125, 0.025, 0.0125, 0.05],
    ...             [0, 0.0125, 0.025, 0],
    ...         ]
    ...     )
    ... ) * 2
    >>> dataset = generate_LBM_dataset(
    ...     number_of_rows=10 ** 3,
    ...     number_of_columns=5 * 10 ** 3,
    ...     nb_row_clusters=3,
    ...     nb_column_clusters=4,
    ...     connection_probabilities=connection_probabilities,
    ...     row_cluster_proportions=np.ones(3)/3,
    ...     column_cluster_proportions=np.ones(4)/4
    ... )


    """
    number_of_rows = number_of_rows if number_of_rows else 2 * 10**3
    number_of_columns = number_of_columns if number_of_columns else 10**3
    nb_row_clusters = nb_row_clusters if nb_row_clusters else np.random.randint(3, 6)
    nb_column_clusters = (
        nb_column_clusters if nb_column_clusters else np.random.randint(3, 6)
    )
    if connection_probabilities is None:
        connection_probabilities = (
            np.random.choice(
                nb_row_clusters * nb_column_clusters,
                nb_row_clusters * nb_column_clusters,
                replace=False,
            )
            .reshape(nb_row_clusters, nb_column_clusters)
            .astype(float)
        )
        c = 0.02 / connection_probabilities.mean()
        connection_probabilities *= c
    row_cluster_proportions = (
        row_cluster_proportions
        if row_cluster_proportions is not None
        else (np.ones(nb_row_clusters) / nb_row_clusters)
    )
    column_cluster_proportions = (
        column_cluster_proportions
        if column_cluster_proportions is not None
        else (np.ones(nb_column_clusters) / nb_column_clusters)
    )

    try:  # pylint: disable=too-many-nested-blocks
        if verbosity > 0:
            logger.info("---------- START Graph Generation ---------- ")
            bar = progressbar.ProgressBar(  # pylint: disable=blacklisted-name
                max_value=nb_row_clusters * nb_column_clusters,
                widgets=[
                    progressbar.SimpleProgress(),
                    " Generating block: ",
                    " [",
                    progressbar.Percentage(),
                    " ] ",
                    progressbar.Bar(),
                    " [ ",
                    progressbar.Timer(),
                    " ] ",
                ],
                redirect_stdout=True,
            ).start()
        row_cluster_indicator = np.random.multinomial(
            1, row_cluster_proportions.flatten(), size=number_of_rows
        )
        column_cluster_indicator = np.random.multinomial(
            1, column_cluster_proportions.flatten(), size=number_of_columns
        )
        if not sparse:
            X = np.random.binomial(
                1,
                row_cluster_indicator
                @ connection_probabilities
                @ column_cluster_indicator.T,
            )
            graph = scipy.sparse.coo_matrix(
                X, shape=(number_of_rows, number_of_columns)
            )
        else:
            row_classes = [
                row_cluster_indicator[:, q].nonzero()[0] for q in range(nb_row_clusters)
            ]
            col_classes = [
                column_cluster_indicator[:, l].nonzero()[0]
                for l in range(nb_column_clusters)
            ]

            rows = np.array([])
            cols = np.array([])
            for i, (q, l) in enumerate(
                [
                    (i, j)
                    for i in range(nb_row_clusters)
                    for j in range(nb_column_clusters)
                ]
            ):
                if verbosity > 0:
                    bar.update(i)
                n1, n2 = row_classes[q].size, col_classes[l].size
                nnz = np.random.binomial(n1 * n2, connection_probabilities[q, l])
                if nnz > 0:
                    row = np.random.choice(row_classes[q], size=2 * nnz)
                    col = np.random.choice(col_classes[l], size=2 * nnz)
                    row_col_unique = np.unique(np.stack((row, col), 1), axis=0)
                    while row_col_unique.shape[0] < nnz:
                        row = np.random.choice(row_classes[q], size=2 * nnz)
                        col = np.random.choice(col_classes[l], size=2 * nnz)
                        row_col_unique = np.unique(np.stack((row, col), 1), axis=0)
                    np.random.shuffle(row_col_unique)
                    rows = np.concatenate((rows, row_col_unique[:nnz, 0]))
                    cols = np.concatenate((cols, row_col_unique[:nnz, 1]))

            graph = scipy.sparse.coo_matrix(
                (np.ones(rows.size), (rows, cols)),
                shape=(number_of_rows, number_of_columns),
            )
        if verbosity > 0:
            bar.finish()

    except KeyboardInterrupt:
        return None
    finally:
        if verbosity > 0:
            bar.finish()

    dataset = LBM_dataset(
        data=graph,
        row_cluster_indicator=row_cluster_indicator,
        column_cluster_indicator=column_cluster_indicator,
    )

    return dataset


def generate_SBM_dataset(  # pylint: disable=too-many-statements,too-many-branches,too-many-locals,too-many-arguments,invalid-name
    # pylint: disable=unsubscriptable-object
    number_of_nodes: Optional[int] = None,
    number_of_clusters: Optional[int] = None,
    connection_probabilities: Optional[np.ndarray] = None,
    cluster_proportions: Optional[np.ndarray] = None,
    symmetric: Optional[bool] = False,
    verbosity: Optional[int] = 1,
) -> SBM_dataset:
    """Generate a sparse graph with Stochastic Block Models.

    Parameters
    ----------
    number_of_nodes : int, optional, default : 1000
        The number of nodes.
    number_of_clusters : int, optional, default : random between 3 and 5
        The number of classes of nodes.
    connection_probabilities : np.ndarray, optional, default : see notes
        The probability of having an edge between the classes.
    cluster_proportions : np.ndarray, optional, default : balanced probabilies
        Proportion of the classes of nodes.
    symmetric : bool, optional, default : False
        Specify if the generated adjacency matrix is symmetric.
    verbosity : int, optional, default : 1
        Display information during the generation process.

    Returns
    -------
    LBM_dataset
        The generated dataset.

    Notes
    -----
    If no connection_probabilities is given, an affiliation graph is generated
    with random probabilies on diagonal and such as the sparsity of the adjacency
    matrix is 0.01.

    Examples
    --------
    >>> generate_SBM_dataset()

    >>> connection_probabilities = np.array(
    ...     [
    ...         [0.05, 0.018, 0.006, 0.0307],
    ...         [0.018, 0.037, 0, 0],
    ...         [0.006, 0, 0.055, 0.012],
    ...         [0.0307, 0, 0.012, 0.043],
    ...     ]
    ... )
    >>> dataset = generate_SBM_dataset(
    ...     number_of_nodes= 10 ** 3,
    ...     number_of_clusters=4,
    ...     cluster_proportions=np.ones(4)/4,
    ...     connection_probabilities=connection_probabilities,
    ...     symmetric=True,
    ... )

    """
    number_of_nodes = number_of_nodes if number_of_nodes else 10**3
    number_of_clusters = (
        number_of_clusters if number_of_clusters else np.random.randint(3, 6)
    )
    cluster_proportions = (
        cluster_proportions
        if cluster_proportions is not None
        else (np.ones(number_of_clusters) / number_of_clusters)
    )
    if connection_probabilities is None:
        connection_probabilities = (
            np.ones((number_of_clusters, number_of_clusters)) * np.random.rand()
        )
        d = connection_probabilities[0, 0] * np.random.randint(
            2, 20, number_of_clusters
        )
        np.fill_diagonal(connection_probabilities, d)
        c = 0.01 / connection_probabilities.mean()
        connection_probabilities *= c

    try:  # pylint: disable=too-many-nested-blocks
        if verbosity > 0:
            logger.info("---------- START Graph Generation ---------- ")
            bar = progressbar.ProgressBar(  # pylint: disable=blacklisted-name
                max_value=number_of_clusters**2,
                widgets=[
                    progressbar.SimpleProgress(),
                    " Generating block: ",
                    " [",
                    progressbar.Percentage(),
                    " ] ",
                    progressbar.Bar(),
                    " [ ",
                    progressbar.Timer(),
                    " ] ",
                ],
                redirect_stdout=True,
            ).start()
        cluster_indicator = np.random.multinomial(
            1, cluster_proportions.flatten(), size=number_of_nodes
        )
        classes = [
            cluster_indicator[:, q].nonzero()[0] for q in range(number_of_clusters)
        ]

        rows = np.array([])
        cols = np.array([])
        for i, (q, l) in enumerate(
            [
                (i, j)
                for i in range(number_of_clusters)
                for j in range(number_of_clusters)
            ]
        ):
            if verbosity > 0:
                bar.update(i)
            n1, n2 = classes[q].size, classes[l].size

            if connection_probabilities[q, l] >= 0.25:
                for idclass in classes[q]:
                    nb_ones = np.random.binomial(
                        classes[l].size, connection_probabilities[q, l]
                    )
                    col = np.random.choice(classes[l], nb_ones, replace=False)
                    row = np.ones_like(col) * idclass
                    row_col_unique = np.unique(np.stack((row, col), 1), axis=0)
                    np.random.shuffle(row_col_unique)
                    rows = np.concatenate((rows, row_col_unique[:, 0]))
                    cols = np.concatenate((cols, row_col_unique[:, 1]))
            else:
                nnz = np.random.binomial(n1 * n2, connection_probabilities[q, l])
                if nnz > 0:
                    row = np.random.choice(classes[q], size=2 * nnz)
                    col = np.random.choice(classes[l], size=2 * nnz)
                    row_col_unique = np.unique(np.stack((row, col), 1), axis=0)
                    while row_col_unique.shape[0] < nnz:
                        row = np.random.choice(classes[q], size=2 * nnz)
                        col = np.random.choice(classes[l], size=2 * nnz)
                        row_col_unique = np.unique(np.stack((row, col), 1), axis=0)
                    np.random.shuffle(row_col_unique)
                    rows = np.concatenate((rows, row_col_unique[:nnz, 0]))
                    cols = np.concatenate((cols, row_col_unique[:nnz, 1]))

        inserted = np.stack((rows, cols), axis=1)
        if symmetric:
            inserted = inserted[inserted[:, 0] < inserted[:, 1]]
            inserted = np.concatenate((inserted, inserted[:, [1, 0]]))
        else:
            inserted = inserted[inserted[:, 0] != inserted[:, 1]]

        graph = scipy.sparse.coo_matrix(
            (np.ones(inserted[:, 0].size), (inserted[:, 0], inserted[:, 1])),
            shape=(number_of_nodes, number_of_nodes),
        )
        if verbosity > 0:
            bar.finish()

    except KeyboardInterrupt:
        return None
    finally:
        if verbosity > 0:
            bar.finish()

    return SBM_dataset(data=graph, cluster_indicator=cluster_indicator)
