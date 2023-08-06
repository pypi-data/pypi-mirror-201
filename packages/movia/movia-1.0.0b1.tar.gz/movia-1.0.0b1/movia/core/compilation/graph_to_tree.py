#!/usr/bin/env python3

"""
** Compile an assembly graph into an evaluable tree **
------------------------------------------------------
"""


import typing

import networkx

from movia.core.classes.container import ContainerOutput
from movia.core.classes.node import Node
from movia.core.classes.stream import Stream
from movia.core.optimisation.cache.hashes import compute_nodes_hash



def _tree_from_node(node_name: str, graph: networkx.MultiDiGraph) -> None:
    """
    ** Recursively retrieve the node corresponding to the node of the graph. **

    Complete the ``tree`` attribute for this node and for the out streams of this node.
    This function is recursive, so all ancestors are also completed.

    Parameters
    ----------
    node : str
        The name of the node that allows to determine the corresponding subgraph.
    graph : networkx.MultiDiGraph
        The complete assembly graph.

    Notes
    -----
    If the node is a terminal node, it is the complete dynamic tree.
    """
    assert isinstance(graph, networkx.MultiDiGraph), graph.__class__.__name__
    assert isinstance(node_name, str), node_name.__class__.__name__
    assert node_name in graph.nodes(), sorted(graph.nodes())

    # create node and recursively the parent nodes
    node = graph.nodes[node_name]
    if node["tree"] is None:
        for pred in graph.predecessors(node_name):
            _tree_from_node(pred, graph) # editing by pointer
        in_edges = graph.in_edges(node_name, keys=True)
        if sorted(int(k.split("->")[1]) for _, _, k in in_edges) != list(range(len(in_edges))):
            raise IndexError(
                f"the streams ({in_edges}) arriving on {node_name} are not correctly incremented"
            )
        in_streams = [
            graph.edges[edge_name]["tree"] for edge_name in
            sorted(in_edges, key=lambda src_dst_key: int(src_dst_key[2].split("->")[1]))
        ] # the streams that arrive on the current node
        node["tree"] = new_node(node["class"], in_streams, node["state"])
        assert node["tree"].in_streams == tuple(in_streams), \
            f"the node {node_name} does not have the specified input streams"

    # complete out streams
    for out_edge_name in graph.out_edges(node_name, keys=True):
        out_edge = graph.edges[out_edge_name]
        if out_edge["tree"] is None:
            index = int(out_edge_name[2].split("->")[0])
            assert index < len(node["tree"].out_streams), (
                f"the {out_edge_name[0]} node has only {len(node['tree'].out_streams)} "
                f"output streams, impossible to access stream index {index}"
            )
            out_edge["tree"] = node["tree"].out_streams[index]


def graph_to_tree(graph: networkx.MultiDiGraph) -> ContainerOutput:
    """
    ** Creates the dynamic tree from the assembly graph. **

    The abstract dynamic tree alows the evaluation of the complete pipeline.

    Parameters
    ----------
    graph : networkx.MultiDiGraph
        The assembly graph.

    Returns
    -------
    container_out : movia.core.classes.container.ContainerOutput
        An evaluable multimedia muxer.

    Examples
    --------
    >>> from movia.core.classes.container import ContainerOutput
    >>> from movia.core.compilation.graph_to_tree import graph_to_tree
    >>> from movia.core.compilation.tree_to_graph import tree_to_graph
    >>> from movia.core.generation.audio.noise import GeneratorAudioNoise
    >>> tree = tree_to_graph(ContainerOutput(GeneratorAudioNoise.default().out_streams))
    >>> graph_to_tree(tree) # doctest: +ELLIPSIS
    <movia.core.classes.container.ContainerOutput object at ...>
    >>>
    """
    # verification and extraction of the termination node
    assert isinstance(graph, networkx.MultiDiGraph), graph.__class__.__name__
    out_nodes = [n for n in graph.nodes if issubclass(graph.nodes[n]["class"], ContainerOutput)]
    assert len(out_nodes) == 1, f"only one output node is possible, not {len(out_nodes)}"
    out_node = out_nodes.pop()
    assert issubclass(graph.nodes()[out_node]["class"], ContainerOutput), \
        graph.nodes[out_node]["class"].__name__

    # fill
    update_tree(graph)
    container_out = graph.nodes[out_node]["tree"]
    return container_out


def new_node(node_class: type, in_streams: typing.Iterable[Stream], state: dict) -> Node:
    """
    ** Instantiates and initializes a new node. **

    Parameters
    ----------
    node_class : type
        The uninstantiated class describing the node to be created.
        This class must be inherited from the ``movia.core.classes.node.Node`` class.
    in_streams : typing.Iterable[Stream]
        See ``movia.core.classes.node.Node.setstate``.
    state : dict
        See ``movia.core.classes.node.Node.setstate``.

    Returns
    -------
    node : Node
        A new instantiated and initialized node.
    """
    assert isinstance(node_class, type), f"{node_class} must be a class, not an object"
    assert issubclass(node_class, Node), f"{node_class.__name__} class does not inherit from Node"

    node = node_class.__new__(node_class)
    node.setstate(in_streams, state)
    return node


def update_tree(graph: networkx.MultiDiGraph) -> None:
    """
    ** Updates on each node the ``tree`` attribute. **

    From the assembly graph, this function reconstructs the dynamic instances
    and is able to perform the calculations.
    By adding to each node the attribute ``tree``,
    it allows not only to keep the graph structure but also
    to recalculate only the parts that need to be changed.

    The operation are applies in-place.

    Parameters
    ----------
    graph : networkx.MultiDiGraph
        The assembly graph who is going to have the updated ``tree`` attributes.

    Examples
    --------
    >>> import pprint
    >>> import networkx as nx
    >>> from movia.core.classes.container import ContainerOutput
    >>> from movia.core.compilation.graph_to_tree import update_tree
    >>> from movia.core.compilation.tree_to_graph import tree_to_graph
    >>> from movia.core.io.read import ContainerInputFFMPEG
    >>> with ContainerInputFFMPEG("movia/examples/video.mp4") as container_in:
    ...     container_out = ContainerOutput(container_in.out_streams)
    ...     graph = tree_to_graph(container_out)
    ...
    >>> pprint.pprint(nx.get_node_attributes(graph, 'tree'))
    {}
    >>> pprint.pprint(nx.get_edge_attributes(graph, 'tree'))
    {}
    >>> update_tree(graph)
    >>> pprint.pprint(nx.get_node_attributes(graph, 'tree')) # doctest: +ELLIPSIS
    {'container_input_ffmpeg_1': <movia.core.io.read.ContainerInputFFMPEG object at ...>,
     'container_output_1': <movia.core.classes.container.ContainerOutput object at ...>}
    >>> pprint.pprint(nx.get_edge_attributes(graph, 'tree')) # doctest: +ELLIPSIS
    {(...): <movia.core.io.read._StreamVideoFFMPEG object at ...>}
    >>>
    """
    assert isinstance(graph, networkx.MultiDiGraph), graph.__class__.__name__

    # clean obsolete tree and declaration
    hashes = compute_nodes_hash(graph)
    for node_name, new_hash in hashes.items():
        node = graph.nodes[node_name]
        if node.get("hash", None) == new_hash: # if hash match
            for (*edge, tree) in graph.out_edges(node_name, keys=True, data="tree", default=None):
                graph.add_edge(*edge, tree=tree)
        else: # obsolete case (need update)
            node["hash"] = new_hash
            node["tree"] = None
            for edge_name in graph.out_edges(node_name, keys=True):
                graph.add_edge(*edge_name, tree=None)

    # complete graph
    out_nodes = [node for node in graph.nodes() if graph.out_degree(node) == 0]
    assert out_nodes, "the graph is empty or contains cycle"
    for node_name in out_nodes:
        _tree_from_node(node_name, graph)
