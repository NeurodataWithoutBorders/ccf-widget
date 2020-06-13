__all__ = ['labels_for_allen_id']

import urllib.request
import json

from .structure_graph import allen_id_to_tree_node

from IPython.core.debugger import set_trace

# Todo: Use AWS store after Scott / Lydia upload
with urllib.request.urlopen("https://thewtex.github.io/allen-ccf-itk-vtk-zarr/allen_id_to_label.json") as url:
    allen_id_to_label_str_keys = json.loads(url.read().decode())
allen_id_to_label = { int(k): v for k,v in allen_id_to_label_str_keys.items() }

def labels_for_allen_id_internal(allen_id, labels):
    node = allen_id_to_tree_node[allen_id]
    if len(node.children) == 0:
        if node.allen_id in allen_id_to_label:
            labels.append(allen_id_to_label[node.allen_id])
    else:
        for child in node.children:
            labels_for_allen_id_internal(child.allen_id, labels)
    return labels

labels_for_allen_id_cache = dict()
def labels_for_allen_id(allen_id):
    if allen_id in labels_for_allen_id_cache:
        return labels_for_allen_id_cache[allen_id]
    else:
        labels = []
        labels_for_allen_id_internal(allen_id, labels)
        labels_for_allen_id_cache[allen_id] = labels
        return labels
