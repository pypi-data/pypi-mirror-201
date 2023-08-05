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

import collections
from dataclasses import dataclass
from typing import Union

import numpy as np
import scipy.sparse

from sparsebm import SBM, LBM


@dataclass(frozen=True)
class LBM_dataset:  # pylint: disable=invalid-name
    """Dataclass type to store a generated LBM network.

    Attributes
    ----------
    data: scipy.sparse.coo_matrix
        adjacency matrix with shape (rows, columns).
    row_cluster_indicator: np.ndarray
        The indicator matrix of the clustering on rows.
        The shape is (rows, row_clusters).
    column_cluster_indicator: np.ndarray
        The indicator matrix of the clustering on columns.
        The shape is (columns, column_clusters).
    rows: int
        (property) The number of nodes of type (1) which is the number of rows
        of the adjacency matrix.
    columns: int
        (property) The number of nodes of type (2) which is the number of
        columns of the adjacency matrix.
    row_clusters: int
        (property) The number of classes of nodes of type (1).
    column_clusters: int
        (property) The number of classes of nodes of type (2).
    row_labels: np.ndarray
        (property) Labels of nodes of type (1). The shape is (rows, ).
    column_labels: np.ndarray
        (property) Labels of nodes of type (2). The shape is (columns, ).
    """

    data: scipy.sparse.coo_matrix
    row_cluster_indicator: np.ndarray
    column_cluster_indicator: np.ndarray

    @property
    def rows(self) -> int:
        """The number of nodes of type (1) which is the number of rows of the
        adjacency matrix."""
        return self.data.shape[0]

    @property
    def columns(self) -> int:
        """The number of nodes of type (2) which is the number of columns of the
        adjacency matrix."""
        return self.data.shape[1]

    @property
    def row_clusters(self) -> int:
        """The number of classes of nodes of type (1)."""
        return self.row_cluster_indicator.shape[1]

    @property
    def column_clusters(self) -> int:
        """The number of classes of nodes of type (2)."""
        return self.column_cluster_indicator.shape[1]

    @property
    def row_labels(self) -> np.ndarray:
        """Labels of nodes of type (2). The shape is (columns, )."""
        return np.argmax(self.row_cluster_indicator, axis=1)

    @property
    def column_labels(self) -> np.ndarray:
        """Labels of nodes of type (1). The shape is (rows, )."""
        return np.argmax(self.column_cluster_indicator, axis=1)

    def __getitem__(self, item):
        # Method added for backward compat, dict were used.
        if hasattr(self, item):
            return getattr(self, item)
        raise KeyError(f"{self.__class__.__name__} does not have item {item!r}")


@dataclass(frozen=True)
class SBM_dataset:  # pylint: disable=invalid-name
    """Dataclass type to store a generated SBM network.

    Attributes
    ----------
    data: scipy.sparse.coo_matrix
        adjacency matrix with shape (nodes, nodes).
    cluster_indicator: np.ndarray
        The indicator matrix of the clustering on nodes.
        The shape is (nodes, clusters).
    nodes: int
        (property) The number of nodes is the number of rows and columns
        of the adjacency matrix.
    clusters: int
        (property) The number of classes of nodes.
    labels: np.ndarray
        (property) Labels of nodes. The shape is (nodes, ).
    """

    data: scipy.sparse.coo_matrix
    cluster_indicator: np.ndarray

    @property
    def nodes(self) -> int:
        """The number of nodes which is the number of rows and columns of the
        adjacency matrix."""
        return self.data.shape[0]

    @property
    def clusters(self) -> int:
        """The number of classes of nodes."""
        return self.cluster_indicator.shape[1]

    @property
    def labels(self) -> np.ndarray:
        """Labels of nodes of type (2). The shape is (columns, )."""
        return np.argmax(self.cluster_indicator, axis=1)

    def __getitem__(self, item):
        # Method added for backward compat, dict were used.
        if hasattr(self, item):
            return getattr(self, item)
        raise KeyError(f"{self.__class__.__name__} does not have item {item!r}")


class ModelSelectionResults(collections.abc.Mapping):
    """Class to store the model selection results.

    The best result (from ICL) is given by the property `best`. All result can
    be accessed using dict-interface (getitem, `keys()`, `values()`, `items()`).

    Examples
    --------
    For SBM model selection:

    >>> sbm_model_selection = ModelSelection(
    ... model_type="SBM",
    ... plot=True,
    ... )
    >>> sbm_selection = sbm_model_selection.fit(graph)
    >>> sbm_selection.best # to access the best (ICL) fitted model
    >>> sbm_selection[4] # to access the fitted model for 4 groups

    For LBM model selection:

    >>> lbm_model_selection = ModelSelection(
    ... model_type="LBM",
    ... plot=True,
    ... )
    >>> lbm_selection = lbm_model_selection.fit(graph)
    >>> lbm_selection.best # to access the best (ICL) fitted model
    >>> lbm_selection[4,3] # to access the fitted model
    ...                    # for 4 row-group and 3 col-group
    """

    def __init__(self, explored):
        self._models = explored
        self._best = max(explored.values(), key=lambda x: x.get_ICL())

    @property
    def best(self) -> Union[SBM, LBM]:
        """Model with higher ICL value."""
        return self._best

    def __getitem__(self, key):
        return self._models[key]

    def keys(self):
        return self._models.keys()

    def values(self):
        return self._models.values()

    def items(self):
        return self._models.items()

    def __len__(self):
        return len(self._models)

    def __iter__(self):
        return iter(self._models)
