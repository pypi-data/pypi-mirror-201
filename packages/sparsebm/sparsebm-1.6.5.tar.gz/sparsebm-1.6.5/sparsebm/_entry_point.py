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

import json
import logging
import argparse

import numpy as np
import pandas as pd
import scipy.sparse as sp

from sparsebm import (
    SBM,
    LBM,
    ModelSelection,
    generate_LBM_dataset,
    generate_SBM_dataset,
)


logger = logging.getLogger(__name__)

try:
    import cupy  # pylint: disable=unused-import

    _DEFAULT_USE_GPU = True
except ImportError:
    _DEFAULT_USE_GPU = False


def _define_parsers():
    main_parser = argparse.ArgumentParser(prog="sparsebm")
    subparsers = main_parser.add_subparsers(
        help="algorithm to use", dest="subparser_name"
    )

    sbm_parser = subparsers.add_parser("sbm", help="use the stochastic block model")
    lbm_parser = subparsers.add_parser("lbm", help="use the latent block model")
    ms_parser = subparsers.add_parser(
        "modelselection", help="use the model selection with LBM or SBM"
    )
    input_grp = ms_parser.add_argument_group("mandatory arguments")
    input_grp.add_argument("ADJACENCY_MATRIX", help="List of edges in CSV format")
    input_grp.add_argument(
        "-t",
        "--type",
        help="model to use. Either 'lbm' or 'sbm'",
        required=True,
    )
    input_grp = ms_parser.add_argument_group("optional arguments")
    input_grp.add_argument(
        "-sep",
        "--sep",
        default=",",
        help="CSV delimiter to use. Default is ',' ",
    )
    input_grp.add_argument(
        "-gpu",
        "--use_gpu",
        help="specify if a GPU should be used.",
        default=_DEFAULT_USE_GPU,
        type=bool,
    )
    input_grp.add_argument(
        "-idgpu",
        "--gpu_index",
        help="specify the gpu index if needed.",
        default=None,
        type=bool,
    )
    input_grp.add_argument(
        "-s",
        "--symmetric",
        help="specify if the adajacency matrix is symmetric. For sbm only",
        default=False,
    )
    input_grp.add_argument(
        "-p", "--plot", help="display model exploration plot", default=True
    )
    output_grp = ms_parser.add_argument_group("output")
    output_grp.add_argument(
        "-o",
        "--output",
        help="File path for the json results.",
        default="results.json",
    )

    generate_sbm_parser = subparsers.add_parser(
        "generate", help="use sparsebm to generate a data matrix"
    )
    subparsers_generate = generate_sbm_parser.add_subparsers(
        help="model to generate data with",
        dest="subparsers_generate_name",
    )
    sbm_generation_parser = subparsers_generate.add_parser(
        "sbm", help="use the stochastic block model to generate data"
    )
    lbm_generation_parser = subparsers_generate.add_parser(
        "lbm", help="use the latent block model to generate data"
    )

    help_example_base = """A json configuration file that specify the parameters
    of the data to generate. If no file is given a random graph is generated."""
    help_sbm_gen = """\n Example of json configuration file for SBM: \n{\n
    "type": "sbm",\n  "number_of_nodes": 1000,\n  "number_of_clusters": 4,\n
    "symmetric": true,\n  "connection_probabilities": [\n    [\n      0.1,\n
      0.036,\n      0.012,\n      0.0614\n    ],\n    [\n      0.036,\n
        0.074,\n      0,\n      0\n    ],\n    [\n      0.012,\n      0,\n
          0.11,\n      0.024\n    ],\n    [\n      0.0614,\n      0,\n
          0.024,\n      0.086\n    ]\n  ],\n  "cluster_proportions": [\n    0.25
          ,\n    0.25,\n    0.25,\n    0.25\n  ]\n}"""

    sbm_generation_parser.add_argument(
        "-f",
        "--file",
        default=None,
        help=help_example_base + help_sbm_gen,
        required=False,
    )
    lbm_generation_parser.add_argument(
        "-f", "--file", default=None, help=help_example_base, required=False
    )
    for parser in [sbm_parser, lbm_parser]:
        input_grp = parser.add_argument_group("mandatory arguments")
        input_grp.add_argument("ADJACENCY_MATRIX", help="List of edges in CSV format")
        if parser == lbm_parser:
            input_grp.add_argument(
                "-k1",
                "--n_row_clusters",
                help="number of row clusters",
                default=4,
                type=int,
                required=True,
            )
            input_grp.add_argument(
                "-k2",
                "--n_column_clusters",
                help="number of row clusters",
                default=4,
                type=int,
                required=True,
            )
        if parser == sbm_parser:
            input_grp.add_argument(
                "-k",
                "--n_clusters",
                help="number of clusters",
                default=4,
                type=int,
                required=True,
            )

        output_grp = parser.add_argument_group("output")
        output_grp.add_argument(
            "-o",
            "--output",
            help="File path for the json results.",
            default="results.json",
        )

        param_grp = parser.add_argument_group("optional arguments")
        param_grp.add_argument(
            "-sep",
            "--sep",
            default=",",
            help="CSV delimiter to use. Default is ',' ",
        )
        if parser == sbm_parser:
            param_grp.add_argument(
                "-s",
                "--symmetric",
                help="Specify if the adajacency matrix is symmetric",
                default=False,
                # type=bool,
            )
        param_grp.add_argument(
            "-niter",
            "--max_iter",
            help="Maximum number of EM step",
            default=10000,
            type=int,
        )
        param_grp.add_argument(
            "-ninit",
            "--n_init",
            help="Number of initializations that will be run",
            default=100,
            type=int,
        )
        param_grp.add_argument(
            "-early",
            "--n_iter_early_stop",
            help="Number of EM steps to perform for each initialization.",
            default=10,
            type=int,
        )
        param_grp.add_argument(
            "-ninitt",
            "--n_init_total_run",
            help="Number of the best initializations that will be run\
            until convergence.",
            default=2,
            type=int,
        )
        param_grp.add_argument(
            "-t",
            "--tol",
            help="Tolerance of likelihood to declare convergence.",
            default=1e-4,
            type=float,
        )
        param_grp.add_argument(
            "-v",
            "--verbosity",
            help="Degree of verbosity. Scale from 0 (no message displayed)\
             to 3.",
            default=1,
            type=int,
        )
        param_grp.add_argument(
            "-gpu",
            "--use_gpu",
            help="Specify if a GPU should be used.",
            default=_DEFAULT_USE_GPU,
            type=bool,
        )
        param_grp.add_argument(
            "-idgpu",
            "--gpu_index",
            help="Specify the gpu index if needed.",
            default=None,
            type=bool,
        )

    return main_parser


def _graph_from_csv(file_, type_, sep=","):
    try:
        pda = pd.read_csv(file_, sep=sep, header=None)

        npa = pda[[0, 1]].to_numpy()
        if type_ == "sbm":
            node_i_from = np.unique(npa)
            node_i_to = np.arange(node_i_from.size)
            i_mapping = dict(np.stack((node_i_from, node_i_to), 1))
            rows = pda[0].map(i_mapping)
            cols = pda[1].map(i_mapping)
            graph = sp.coo_matrix(
                (np.ones(npa.shape[0]), (rows, cols)),
                shape=(node_i_from.size, node_i_from.size),
            )
            return graph, i_mapping, None
        node_i_from = np.unique(npa[:, 0])
        node_i_to = np.arange(node_i_from.size)
        i_mapping = dict(np.stack((node_i_from, node_i_to), 1))
        rows = pda[0].map(i_mapping)
        node_j_from = np.unique(npa[:, 1])
        node_j_to = np.arange(node_j_from.size)
        j_mapping = dict(np.stack((node_j_from, node_j_to), 1))
        cols = pda[1].map(j_mapping)
        graph = sp.coo_matrix(
            (np.ones(npa.shape[0]), (rows, cols)),
            shape=(node_i_from.size, node_j_from.size),
        )
        return graph, i_mapping, j_mapping
    except Exception as expt:
        logger.error(expt)
        raise expt


def _str2bool(value):
    if isinstance(value, bool):
        return value
    if value.lower() in {"yes", "true", "t", "y", "1"}:
        return True
    if value.lower() in {"no", "false", "f", "n", "0"}:
        return False
    raise argparse.ArgumentTypeError("Boolean value expected.")


def _process_sbm(args):  # pylint: disable=inconsistent-return-statements
    graph, row_from_to, _ = _graph_from_csv(
        args["ADJACENCY_MATRIX"], args["subparser_name"], sep=args["sep"]
    )
    model = SBM(
        max_iter=args["max_iter"],
        n_clusters=args["n_clusters"],
        n_init=args["n_init"],
        n_iter_early_stop=args["n_iter_early_stop"],
        n_init_total_run=args["n_init_total_run"],
        verbosity=args["verbosity"],
        atol=args["tol"],
        use_gpu=args["use_gpu"],
        gpu_index=args["gpu_index"],
    )
    symmetric = _str2bool(args["symmetric"])
    logger.info("Runing with symmetric adjacency matrix : %s", symmetric)
    model.fit(graph, symmetric=symmetric)

    if not model.trained_successfully:
        logger.error("FAILED, model has not been trained successfully.")
        return None
    logger.info("Model has been trained successfully.")
    logger.info(  # pylint: disable=logging-fstring-interpolation
        f"Value of the Integrated Completed Loglikelihood is {model.get_ICL():.4f}"
    )
    labels = model.labels
    groups = [np.argwhere(labels == q).flatten() for q in range(args["n_clusters"])]
    row_to_from = {v: k for k, v in row_from_to.items()}
    groups = [pd.Series(g).map(row_to_from).tolist() for g in groups]

    results = {
        "ILC": model.get_ICL(),
        "edge_probability_between_groups": model.pi_.tolist(),
        "group_membership_probability": model.group_membership_probability.flatten().tolist(),
        "node_ids_clustered": groups,
    }

    with open(args["output"], "w", encoding="utf8") as outfile:
        json.dump(results, outfile)
    logger.info("Results saved in %s", args["output"])


def _process_lbm(args):  # pylint: disable=inconsistent-return-statements
    graph, row_from_to, col_from_to = _graph_from_csv(
        args["ADJACENCY_MATRIX"], args["subparser_name"], sep=args["sep"]
    )
    model = LBM(
        max_iter=args["max_iter"],
        n_row_clusters=args["n_row_clusters"],
        n_column_clusters=args["n_column_clusters"],
        n_init=args["n_init"],
        n_iter_early_stop=args["n_iter_early_stop"],
        n_init_total_run=args["n_init_total_run"],
        verbosity=args["verbosity"],
        atol=args["tol"],
        use_gpu=args["use_gpu"],
        gpu_index=args["gpu_index"],
    )
    model.fit(graph)

    if not model.trained_successfully:
        logger.error("FAILED, model has not been trained successfully.")
        return None
    logger.info("Model has been trained successfully.")
    logger.info(  # pylint: disable=logging-fstring-interpolation
        f"Value of the Integrated Completed Loglikelihood is {model.get_ICL():.4f}"
    )

    row_labels = model.row_labels
    row_groups = [
        np.argwhere(row_labels == q).flatten() for q in range(args["n_row_clusters"])
    ]
    row_to_from = {v: k for k, v in row_from_to.items()}
    row_groups = [pd.Series(g).map(row_to_from).tolist() for g in row_groups]

    col_labels = model.column_labels
    col_groups = [
        np.argwhere(col_labels == q).flatten() for q in range(args["n_column_clusters"])
    ]
    col_to_from = {v: k for k, v in col_from_to.items()}
    col_groups = [pd.Series(g).map(col_to_from).tolist() for g in col_groups]

    results = {
        "ILC": model.get_ICL(),
        "edge_probability_between_groups": model.pi_.tolist(),
        "row_group_membership_probability": model.row_group_membership_probability.flatten().tolist(),  # pylint: disable=line-too-long
        "column_group_membership_probability": model.column_group_membership_probability.flatten().tolist(),  # pylint: disable=line-too-long
        "node_type_1_ids_clustered": row_groups,
        "node_type_2_ids_clustered": col_groups,
    }

    with open(args["output"], "w", encoding="utf8") as outfile:
        json.dump(results, outfile)
    logger.info("Results saved in %s", args["output"])


def _generate_sbm(args):  # pylint: disable=too-many-locals
    if "JSON_FILE" in args:
        with open(args["JSON_FILE"], encoding="utf8") as fjson:
            conf = json.load(fjson)
    else:
        conf = {}

    number_of_nodes = conf["number_of_nodes"] if "number_of_nodes" in conf else None
    number_of_clusters = (
        conf["number_of_clusters"] if "number_of_clusters" in conf else None
    )
    connection_probabilities = (
        np.array(conf["connection_probabilities"])
        if "connection_probabilities" in conf
        else None
    )
    cluster_proportions = (
        np.array(conf["cluster_proportions"]) if "cluster_proportions" in conf else None
    )
    symmetric = conf["symmetric"] if "symmetric" in conf else False
    dataset = generate_SBM_dataset(
        number_of_nodes,
        number_of_clusters,
        connection_probabilities,
        cluster_proportions,
        symmetric=symmetric,
    )
    graph = dataset["data"]
    graph = np.stack((graph.row, graph.col), 1)
    cluster_indicator = dataset["cluster_indicator"]
    labels = cluster_indicator.argmax(1)
    number_of_clusters = cluster_indicator.shape[1]
    groups = [
        np.argwhere(labels == q).flatten().tolist() for q in range(number_of_clusters)
    ]
    results = {
        "node_ids_grouped": groups,
        "number_of_nodes": number_of_nodes,
        "number_of_clusters": number_of_clusters,
        "connection_probabilities": connection_probabilities.flatten().tolist()
        if connection_probabilities
        else None,
        "cluster_proportions": cluster_proportions.tolist()
        if cluster_proportions
        else None,
    }

    file_groups = "./groups.json"
    file_edges = "./edges.csv"
    with open(file_groups, "w", encoding="utf8") as outfile:
        json.dump(results, outfile)
    logger.info("\n Groups and params saved in %s", file_groups)
    np.savetxt(file_edges, graph, delimiter=",")
    logger.info("Edges saved in %s", file_edges)


def _generate_lbm(args):  # pylint: disable=too-many-locals
    if "JSON_FILE" in args:
        with open(args["JSON_FILE"], encoding="utf8") as fjson:
            conf = json.load(fjson)
    else:
        conf = {}

    number_of_rows = conf["number_of_rows"] if "number_of_rows" in conf else None
    number_of_columns = (
        conf["number_of_columns"] if "number_of_columns" in conf else None
    )
    nb_row_clusters = conf["nb_row_clusters"] if "nb_row_clusters" in conf else None
    nb_column_clusters = (
        conf["nb_column_clusters"] if "nb_column_clusters" in conf else None
    )
    connection_probabilities = (
        np.array(conf["connection_probabilities"])
        if "connection_probabilities" in conf
        else None
    )
    row_cluster_proportions = (
        np.array(conf["row_cluster_proportions"])
        if "row_cluster_proportions" in conf
        else None
    )
    column_cluster_proportions = (
        np.array(conf["column_cluster_proportions"])
        if "column_cluster_proportions" in conf
        else None
    )
    dataset = generate_LBM_dataset(
        number_of_rows,
        number_of_columns,
        nb_row_clusters,
        nb_column_clusters,
        connection_probabilities,
        row_cluster_proportions,
        column_cluster_proportions,
    )
    graph = dataset["data"]
    number_of_rows, number_of_columns = graph.shape
    graph = np.stack((graph.row, graph.col), 1)
    row_cluster_indicator = dataset["row_cluster_indicator"]
    column_cluster_indicator = dataset["column_cluster_indicator"]
    row_labels = row_cluster_indicator.argmax(1)
    col_labels = column_cluster_indicator.argmax(1)
    nb_row_clusters = row_cluster_indicator.shape[1]
    nb_column_clusters = column_cluster_indicator.shape[1]
    row_groups = [
        np.argwhere(row_labels == q).flatten().tolist() for q in range(nb_row_clusters)
    ]
    col_groups = [
        np.argwhere(col_labels == q).flatten().tolist()
        for q in range(nb_column_clusters)
    ]
    results = {
        "row_ids_grouped": row_groups,
        "column_ids_grouped": col_groups,
        "number_of_rows": number_of_rows,
        "number_of_columns": number_of_columns,
        "nb_row_clusters": nb_row_clusters,
        "nb_column_clusters": nb_column_clusters,
        "connection_probabilities": connection_probabilities.flatten().tolist()
        if connection_probabilities
        else None,
        "row_cluster_proportions": row_cluster_proportions.tolist()
        if row_cluster_proportions
        else None,
        "column_cluster_proportions": column_cluster_proportions.tolist()
        if column_cluster_proportions
        else None,
    }

    file_groups = "./groups.json"
    file_edges = "./edges.csv"
    with open(file_groups, "w", encoding="utf8") as outfile:
        json.dump(results, outfile)
    logger.info("\nGroups and params saved in %s", file_groups)
    np.savetxt(file_edges, graph, delimiter=",")
    logger.info("Edges saved in %s", file_edges)


def _process_model_selection(  # pylint: disable=too-many-locals,inconsistent-return-statements
    args,
):
    if args["type"].upper() not in ["SBM", "LBM"]:
        raise ValueError("Invalid type argument. Must be 'SBM' or 'LBM'")

    graph, row_from_to, col_from_to = _graph_from_csv(
        args["ADJACENCY_MATRIX"], args["type"].lower(), sep=args["sep"]
    )

    model_selection = ModelSelection(
        model_type=args["type"].upper(),
        use_gpu=args["use_gpu"],
        gpu_index=args["gpu_index"],
        plot=args["plot"],
    )
    model = model_selection.fit(graph, symmetric=args["symmetric"]).best

    if not model.trained_successfully:
        logger.error("FAILED, model has not been trained successfully.")
        return None
    logger.info("Model has been trained successfully.")
    logger.info(  # pylint: disable=logging-fstring-interpolation
        f"Value of the Integrated Completed Loglikelihood is {model.get_ICL():.4f}"
    )
    if args["type"] == "lbm":
        logger.info("The model selection picked %s row classes", model.n_row_clusters)
        logger.info(
            "The model selection picked %s column classes", model.n_column_clusters
        )
        nb_row_clusters = model.n_row_clusters
        nb_column_clusters = model.n_column_clusters
        row_labels = model.row_labels
        row_groups = [
            np.argwhere(row_labels == q).flatten() for q in range(nb_row_clusters)
        ]
        row_to_from = {v: k for k, v in row_from_to.items()}
        row_groups = [pd.Series(g).map(row_to_from).tolist() for g in row_groups]

        col_labels = model.column_labels
        col_groups = [
            np.argwhere(col_labels == q).flatten() for q in range(nb_column_clusters)
        ]
        col_to_from = {v: k for k, v in col_from_to.items()}
        col_groups = [pd.Series(g).map(col_to_from).tolist() for g in col_groups]

        results = {
            "ILC": model.get_ICL(),
            "nb_row_clusters": nb_row_clusters,
            "nb_column_clusters": nb_column_clusters,
            "edge_probability_between_groups": model.pi_.tolist(),
            "row_group_membership_probability": model.row_group_membership_probability.flatten().tolist(),  # pylint: disable=line-too-long
            "column_group_membership_probability": model.column_group_membership_probability.flatten().tolist(),  # pylint: disable=line-too-long
            "node_type_1_ids_clustered": row_groups,
            "node_type_2_ids_clustered": col_groups,
        }
    else:
        logger.info("The model selection picked %s classes", model.n_clusters)
        nb_clusters = model.n_clusters
        labels = model.labels
        groups = [np.argwhere(labels == q).flatten() for q in range(nb_clusters)]
        row_to_from = {v: k for k, v in row_from_to.items()}
        groups = [pd.Series(g).map(row_to_from).tolist() for g in groups]

        results = {
            "ILC": model.get_ICL(),
            "nb_clusters": nb_clusters,
            "edge_probability_between_groups": model.pi_.tolist(),
            "group_membership_probability": model.group_membership_probability.flatten().tolist(),
            "node_ids_clustered": groups,
        }

    with open(args["output"], "w", encoding="utf8") as outfile:
        json.dump(results, outfile)
    logger.info("Results saved in %s", args["output"])


def main():  # pylint: disable=missing-function-docstring
    parsers = _define_parsers()
    args = vars(parsers.parse_args())

    if args["subparser_name"] == "sbm":
        _process_sbm(args)
    elif args["subparser_name"] == "lbm":
        _process_lbm(args)
    elif args["subparser_name"] == "modelselection":
        _process_model_selection(args)
    elif args["subparser_name"] == "generate":
        if (
            args["subparsers_generate_name"]
            and args["subparsers_generate_name"].upper() == "SBM"
        ):
            _generate_sbm(args)
        elif (
            args["subparsers_generate_name"]
            and args["subparsers_generate_name"].upper() == "LBM"
        ):
            _generate_lbm(args)
        else:
            raise ValueError(
                "Specify positional argument 'sbm' or 'lbm' to generate data"
            )


if __name__ == "__main__":
    main()
