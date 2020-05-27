from src.drama_network import DramaNetwork
from src.converters.edge_list_converter import convert_to_edge_list
from src.converters.networkx_converter import convert_to_networkx
from src.converters.string_converter import convert_to_string
from pprint import pprint
import toml
import yaml

dn = DramaNetwork("examples/fake_play")
print(convert_to_string(dn))
