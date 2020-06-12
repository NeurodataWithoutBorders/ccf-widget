import urllib.request
import json

# Todo: Use AWS store after Scott / Lydia upload
with urllib.request.urlopen("https://thewtex.github.io/allen-ccf-itk-vtk-zarr/1.json") as url:
    structure_graph = json.loads(url.read().decode())['msg'][0]['children'][0]

acronym_to_allen_id = dict()

def _add_ids(node):
    allen_id = int(node['id'])

    acronym = node['acronym']
    acronym_to_allen_id[acronym] = allen_id

def _process_node(node):
    for child in node['children']:
        _process_node(child)

for node in structure_graph['children']:
    _process_node(node)
