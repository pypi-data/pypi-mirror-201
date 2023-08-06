#!/usr/bin/env python3

"""
** Allows to summarize the state of each element of the graph. **
-----------------------------------------------------------------

This allows a finer management of the cache by a fine tracking of the exchange elements.
"""


import hashlib

import networkx



def compute_nodes_hash(graph: networkx.MultiDiGraph) -> dict[str, str]:
    """
    ** Computes a signature for each node, which reflects its state in the provided graph. **

    This is mean to detecting a change of attributes in one of the upstream elements.

    Parameters
    ----------
    graph : networkx.MultiDiGraph
        The assembly graph.

    Returns
    -------
    hashes : dict[str, str]
        To each node name, associate its state in hexadecimal.

    Notes
    -----
    The graph must not contain any cycles because the function would never returns.

    Examples
    --------
    >>> import pprint
    >>> from movia.core.classes.container import ContainerOutput
    >>> from movia.core.compilation.graph_to_tree import graph_to_tree
    >>> from movia.core.optimisation.cache.hashes import compute_nodes_hash
    >>> from movia.core.compilation.tree_to_graph import tree_to_graph
    >>> from movia.core.io.read import ContainerInputFFMPEG
    >>> with ContainerInputFFMPEG("movia/examples/video.mp4") as container_in:
    ...     container_out = ContainerOutput(container_in.out_streams)
    ...     graph = tree_to_graph(container_out)
    ...
    >>> pprint.pprint(compute_nodes_hash(graph))
    {'container_input_ffmpeg_1': '7d47ddea0d689150b81dab43d8e79c90',
     'container_output_1': '6bf90cc1dc46b4f32ab040def47e11e1'}
    >>>
    """
    assert isinstance(graph, networkx.MultiDiGraph), graph.__class__.__name__

    def complete(hashes, graph, node) -> str:
        if node not in hashes:
            node_attr = graph.nodes[node]
            local_node_signature = (
                f"{node_attr['class'].__name__}-"
                f"{'-'.join(str(node_attr['state'][k]) for k in sorted(node_attr['state']))}"
            )
            in_edges = sorted( # the name of the edges in order of arrival on the node
                graph.in_edges(node, data=False, keys=True),
                key=lambda src_dst_key: int(src_dst_key[2].split("->")[1])
            )
            local_edges_signature = "-".join(k.split("->")[0] for _, _, k in in_edges)
            parents_signature = "-".join(complete(hashes, graph, n) for n, _, _ in in_edges)
            signature = hashlib.md5( # md5 is the fastest
                f"{parents_signature}|{local_edges_signature}|{local_node_signature}".encode()
            ).hexdigest()
            hashes[node] = signature
        return hashes[node]

    hashes = {}
    for node in graph.nodes(data=False):
        complete(hashes, graph, node)
    return hashes
