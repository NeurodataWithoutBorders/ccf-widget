__all__ = ['CCFWidget']

from fsspec.implementations.http import HTTPFileSystem
import json
from ipywidgets import HBox, VBox, register, link, RadioButtons, Checkbox
import itk
from itkwidgets import view
import numpy as np
import xarray as xr
import zarr
import urllib.request

from .ipytree_widget import IPyTreeWidget
from .structure_graph import structure_graph, acronym_to_allen_id

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
        camera = np.array([[-1.9388698e+02, -6.0452373e+03,  2.0659662e+04],
                           [ 6.7440376e+03,  4.0228694e+03,  6.0504180e+03],
                           [ 4.6800941e-01, -8.1573588e-01, -3.3991495e-01]], dtype=np.float32)
        size_limit_3d = [256,256,256]
        self.itk_viewer = view(image=self._image,
                               label_map=self._label_map,
                               opacity_gaussians=opacity_gaussians,
                               label_map_blend=0.8,
                               camera=camera,
                               ui_collapsed=True,
                               size_limit_3d=size_limit_3d,
                               background=(0.1,)*3,
                               gradient_opacity=0.1)
        # Todo: initialization should work
        self.itk_viewer.opacity_gaussians = opacity_gaussians
        self.itk_viewer.rotate = rotate

        mode_buttons = RadioButtons(options=['x', 'y', 'z', 'v'], value='v', description='View mode:')
        link((mode_buttons, 'value'), (self.itk_viewer, 'mode'))

        rotate_checkbox = Checkbox(value=False, description='Rotate')
        link((rotate_checkbox, 'value'), (self.itk_viewer, 'rotate'))
        viewer_controls = HBox([mode_buttons, rotate_checkbox])
        viewer = VBox([self.itk_viewer, viewer_controls])

        children = [viewer]
        self.tree_widget = None
        if tree is not None:
            self.tree_widget = IPyTreeWidget(structure_graph)
            children.append(self.tree_widget)

        super(CCFWidget, self).__init__(children, **kwargs)
