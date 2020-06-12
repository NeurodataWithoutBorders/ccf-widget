import ipytree
from ipywidgets import register

class StructureNodeWidget(ipytree.Node):
    allen_id = 0
    # Allen ID of the parent in the Allen Ontology StructureGraph
    parent_structure_id = 0
    acronym = 'Allen ontology acronym'


@register
class IPyTreeWidget(ipytree.Tree):

    def __init__(self, structure_graph):
        super(IPyTreeWidget, self).__init__(animation=100)
        self.layout.width = '40%'

        self.allen_id_to_node = dict()
        self.acronym_to_allen_id = dict()

        for node in structure_graph['children']:
            self._process_node(self, node)

    def _node_to_widget(self, node):
        node_widget = StructureNodeWidget(node['name'])

        allen_id = int(node['id'])
        node_widget.allen_id = allen_id
        self.allen_id_to_node[allen_id] = node_widget

        node_widget.parent_structure_id = int(node['parent_structure_id'])

        acronym = node['acronym']
        node_widget.acronym = acronym
        self.acronym_to_allen_id[acronym] = allen_id

        return node_widget

    def _process_node(self, parent_widget, node):
        node_widget = self._node_to_widget(node)
        node_widget.opened = False

        parent_widget.add_node(node_widget)
        for child in node['children']:
            self._process_node(node_widget, child)
