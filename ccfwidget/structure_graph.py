__all__ = ['tree', 'allen_id_to_tree_node', 'acronym_to_allen_id', 'allen_id_to_acronym']

import urllib.request
import json

# Todo: Use AWS store after Scott / Lydia upload
with urllib.request.urlopen("https://thewtex.github.io/allen-ccf-itk-vtk-zarr/1.json") as url:
    structure_graph = json.loads(url.read().decode())['msg'][0]['children'][0]

class TreeNode(object):
    children = []
    allen_id = 0
    color_hex_triplet = 'FF0000'

    def __init__(self, allen_id, color_hex_triplet):
        self.allen_id = allen_id
        self.color_hex_triplet = color_hex_triplet
        self.children = []

allen_id_to_tree_node = dict()
acronym_to_allen_id = dict()

def _node_to_tree_node(node):
    allen_id = int(node['id'])
    tree_node = TreeNode(allen_id, node['color_hex_triplet'])
    allen_id_to_tree_node[allen_id] = tree_node

    acronym = node['acronym']
    acronym_to_allen_id[acronym] = allen_id

    return tree_node

def _process_node(tree_parent, node):
    tree_node = _node_to_tree_node(node)
    tree_parent.children.append(tree_node)
    for child in node['children']:
        _process_node(tree_node, child)

tree = TreeNode(None, None)

for node in structure_graph['children']:
    _process_node(tree, node)

allen_id_to_acronym = { v: k for k, v in acronym_to_allen_id.items() }
