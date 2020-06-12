__all__ = ['CCFWidget']

from fsspec.implementations.http import HTTPFileSystem
from ipywidgets import HBox, register
import itk
from itkwidgets import view
import numpy as np
import xarray as xr
import zarr

_image_fs = HTTPFileSystem()
# Todo: Use AWS store after Scott / Lydia upload
_image_store = _image_fs.get_mapper("https://thewtex.github.io/allen-ccf-itk-vtk-zarr/average_template_50_chunked.zarr")
_image_store_cached = zarr.LRUStoreCache(_image_store, max_size=None)
_image_ds = xr.open_zarr(_image_store_cached, consolidated=True)
_image_da = _image_ds.average_template_50

@register
class CCFWidget(HBox):
    """A Jupyter widget for the Allen Common Coordinate Framework (CCF)
    Mouse Brain Atlas."""

    def __init__(self, **kwargs):
        self._image = itk.image_from_xarray(_image_da)
        opacity_gaussians = [[{'position': 0.28094135802469133,
           'height': 0.18181818181818177,
           'width': 0.2988194444444445,
           'xBias': 0.21240499194846996,
           'yBias': 0.5416908212560397},
          {'position': 0.2787808641975309,
           'height': 0.3545454545454545,
           'width': 0.1,
           'xBias': 0,
           'yBias': 0}]]
        camera = np.array([[-1.9388698e+02, -6.0452373e+03,  2.0659662e+04],
           [ 6.7440376e+03,  4.0228694e+03,  6.0504180e+03],
           [ 4.6800941e-01, -8.1573588e-01, -3.3991495e-01]], dtype=np.float32)
        size_limit_3d = [256,256,256]
        self.itk_viewer = view(image=self._image,
                               opacity_gaussians=opacity_gaussians,
                               camera=camera,
                               size_limit_3d=size_limit_3d,
                               background=(0.1,)*3,
                               gradient_opacity=0.1)

        children = [self.itk_viewer]

        super(CCFWidget, self).__init__(children, **kwargs)
