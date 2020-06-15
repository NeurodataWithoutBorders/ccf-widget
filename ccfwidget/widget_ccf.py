__all__ = ['CCFWidget']

from fsspec.implementations.http import HTTPFileSystem
import json
from ipywidgets import HBox, VBox, register, link, RadioButtons, Checkbox, Output
import itk
from itkwidgets import view
import numpy as np
from traitlets import CFloat, CInt, List, Unicode, validate
import xarray as xr
import zarr
import urllib.request

from .ipytree_widget import IPyTreeWidget
from .structure_graph import acronym_to_allen_id, allen_id_to_acronym, structure_graph
from .allen_id_label import labels_for_allen_id

from IPython.core.debugger import set_trace

_image_fs = HTTPFileSystem()
# Todo: Use AWS store after Scott / Lydia upload
_image_store = _image_fs.get_mapper("https://thewtex.github.io/allen-ccf-itk-vtk-zarr/average_template_50_chunked.zarr")
_image_store_cached = zarr.LRUStoreCache(_image_store, max_size=None)
_image_ds = xr.open_zarr(_image_store_cached, consolidated=True)
_image_da = _image_ds.average_template_50

_label_map_fs = HTTPFileSystem()
# Todo: Use AWS store after Scott / Lydia upload
_label_map_store = _label_map_fs.get_mapper("https://thewtex.github.io/allen-ccf-itk-vtk-zarr/allen_ccfv3_annotation_50_contiguous.zarr")
_label_map_store_cached = zarr.LRUStoreCache(_label_map_store, max_size=None)
_label_map_ds = xr.open_zarr(_label_map_store_cached, consolidated=True)
_label_map_da = _label_map_ds.allen_ccfv3_annotation

@register
class CCFWidget(HBox):
    """A Jupyter widget for the Allen Common Coordinate Framework (CCF)
    Mouse Brain Atlas."""

    off_weight = 0.05
    on_weight = 1.0

    selected_acronyms = List(trait=Unicode(), help='Structure Allen Ids to highlight.')
    selected_allen_ids = List(trait=CInt(), help='Structure Allen Ids to highlight.')

    def __init__(self, tree=None, rotate=False, **kwargs):
        self._image = itk.image_from_xarray(_image_da)
        self._label_map = itk.image_from_xarray(_label_map_da)
        opacity_gaussians = [[{'position': 0.28094135802469133,
           'height': 0.3909090909090909,
           'width': 0.44048611111111113,
           'xBias': 0.21240499194846996,
           'yBias': 0.5416908212560397},
          {'position': 0.2787808641975309,
           'height': 1,
           'width': 0.1,
           'xBias': 0,
           'yBias': 0}]]
        opacity_gaussians = [[{'position': 0.32816358024691356,
           'height': 1,
           'width': 0.29048611111111106,
           'xBias': 0.20684943639291442,
           'yBias': 1.1235090030742216}]]
        camera = np.array([[ 1.3441567e+03, -2.1723846e+04,  1.7496496e+04],
                           [ 6.5500000e+03,  3.9750000e+03,  5.6750000e+03],
                           [ 3.6606243e-01, -4.4908229e-01, -8.1506038e-01]], dtype=np.float32)
        size_limit_3d = [256,256,256]
        self.itk_viewer = view(image=self._image,
                               label_map=self._label_map,
                               opacity_gaussians=opacity_gaussians,
                               label_map_blend=0.65,
                               camera=camera,
                               ui_collapsed=True,
                               shadow=False,
                               size_limit_3d=size_limit_3d,
                               background=(0.0,)*3,
                               gradient_opacity=0.1)
        # Todo: initialization should work
        self.itk_viewer.opacity_gaussians = opacity_gaussians
        self.itk_viewer.rotate = rotate
        self.itk_viewer.label_map_blend = 0.65

        mode_buttons = RadioButtons(options=['x', 'y', 'z', 'v'], value='v', description='View mode:')
        link((mode_buttons, 'value'), (self.itk_viewer, 'mode'))

        rotate_checkbox = Checkbox(value=rotate, description='Rotate')
        link((rotate_checkbox, 'value'), (self.itk_viewer, 'rotate'))
        viewer_controls = HBox([mode_buttons, rotate_checkbox])

        viewer = VBox([self.itk_viewer, viewer_controls])

        children = [viewer]

        self._validating_allen_ids = False
        self._validating_acronyms = False
        self._validating_tree = False

        self.tree_widget = None
        if tree is not None:
            if tree == 'ipytree':
                self.tree_widget = IPyTreeWidget(structure_graph)
                children.append(self.tree_widget)
                self.tree_widget.observe(self._ipytree_on_selected_change, names=['selected_nodes'])
                def open_parent(node):
                    if hasattr(node, 'parent_structure_id') and \
                            node.parent_structure_id in self.tree_widget.allen_id_to_node:
                        parent = self.tree_widget.allen_id_to_node[node.parent_structure_id]
                        open_parent(parent)
                    else:
                        node.opened = True

                self.last_selected_tree_nodes = []
                def ipytree_on_allen_ids_changed(change):
                    self._validating_tree = True
                    for node in self.last_selected_tree_nodes:
                        node.selected = False
                    tree_nodes = [self.tree_widget.allen_id_to_node[allen_id] for allen_id in change.new]
                    for node in tree_nodes:
                        open_parent(node)
                        node.selected = True
                        node.opened = True
                    self.last_selected_tree_nodes = tree_nodes
                    self._validating_tree = False
                self.observe(ipytree_on_allen_ids_changed, names='selected_allen_ids')
            else:
                raise RuntimeError('Invalid tree type')

        self.labels = np.unique(self.itk_viewer.rendered_label_map)


        super(CCFWidget, self).__init__(children, **kwargs)

    def _ipytree_on_selected_change(self, change):
        allen_ids = [node.allen_id for node in self.tree_widget.selected_nodes]
        if not self._validating_tree and not self._validating_allen_ids and not self._validating_acronyms:
            self.selected_allen_ids = allen_ids
        self.tree_widget.layout.width = '40%'

    @validate('selected_allen_ids')
    def _validate_selected_allen_ids(self, proposal):
        self._validating_allen_ids = True
        allen_ids = proposal['value']
        self._highlight_allen_ids(allen_ids)
        acronyms = [allen_id_to_acronym[allen_id] for allen_id in allen_ids]
        if not self._validating_acronyms and \
            not self.selected_acronyms == acronyms:
            self.selected_acronyms = acronyms
        self._validating_allen_ids = False
        return allen_ids

    @validate('selected_acronyms')
    def _validate_selected_acronyms(self, proposal):
        self._validating_acronyms = True
        acronyms = proposal['value']
        allen_ids = [acronym_to_allen_id[acronym] for acronym in acronyms]
        if not self._validating_allen_ids and \
            not self.selected_allen_ids == allen_ids:
            self.selected_allen_ids = allen_ids
        self._validating_acronyms = False
        return acronyms

    def _highlight_allen_ids(self, allen_ids):
        weights = np.ones((len(self.labels),), dtype=np.float32)*self.off_weight
        # Background
        weights[0] = 0.0
        for allen_id in allen_ids:
            labels_for_id = labels_for_allen_id(allen_id)
            weights[labels_for_id] = self.on_weight

        self.itk_viewer.label_map_weights = weights
