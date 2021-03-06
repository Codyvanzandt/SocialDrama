from src.sdl_tools.sdl_document import SDLDocument
import src.converters.converters as converters
from src.converters.sdl_file_converter import convert_to_file
from src.utils.networkx_utils import get_subgraph, get_divisions
from src.utils.general_utils import convert_to_container
from src.utils.edge_utils import edges_equal, combine_edges, combine_all_edges
from pprint import pformat
import copy
import networkx


class DramaNetwork:
    def __init__(self, data=None, directed=False):
        self._doc = SDLDocument(data)
        self._data = self._doc.data
        self.directed = directed
        self._graph = converters.drama_network_to_networkx(
            self, directed=self.directed, embed_play=True
        )

    def __iter__(self):
        return iter(self._graph)

    def __contains__(self, n):
        return n in self._graph

    def __len__(self):
        return len(self._graph)

    def __getitem__(self, n):
        return self._graph[n]

    def __getattr__(self, name):
        return getattr(self._graph, name)

    def __str__(self):
        title = self.play().get("title", str())
        return f"{self.__class__.__name__}({title})"

    def play(self):
        return self._graph.graph

    def characters(self, data=False, default=None):
        return self._graph.nodes(data=data, default=default)

    def divisions(self, level=None):
        all_divisions = get_divisions(self._graph)
        if level is None:
            return all_divisions
        else:
            return [
                division
                for division in all_divisions
                if len(division.split(".")) == level
            ]

    def edges(self, nbunch=None, data=False, default=None):
        return self._graph.edges(nbunch=nbunch, data=data, default=default)

    def subnetwork(
        self,
        divisions=None,
        characters=None,
        edges=None,
        character_data=None,
        edge_data=None,
    ):
        divisions = convert_to_container(divisions)
        characters = convert_to_container(characters)
        edges = convert_to_container(edges, nested=True)

        subgraph = get_subgraph(
            self._graph,
            divisions=divisions,
            nodes=characters,
            edges=edges,
            node_data=character_data,
            edge_data=edge_data,
        )
        return converters.networkx_to_drama_network(subgraph)

    def combine_edges(self, equal_func=None, combine_func=None):
        equal_func = equal_func if equal_func is not None else edges_equal
        combine_func = combine_func if combine_func is not None else combine_edges
        new_edges = combine_all_edges(self.edges(data=True), equal_func, combine_func)

        new_graph = (
            networkx.MultiDiGraph(new_edges, **self._graph.graph)
            if self.directed
            else networkx.MultiGraph(new_edges, **self._graph.graph)
        )
        new_graph.add_nodes_from(self.characters(data=True))

        return converters.networkx_to_drama_network(new_graph)

    def to_string(self):
        return self._doc.to_string()

    def to_file(self, path):
        return convert_to_file(self, path)
