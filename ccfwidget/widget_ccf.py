__all__ = ['CCFWidget']

from fsspec.implementations.http import HTTPFileSystem
from ipywidgets import Widget
import itk
from itkwidgets import view
import xarray as xr
import zarr

_image_fs = HTTPFileSystem()
# Todo: Use AWS store after Scott / Lydia upload
_image_store = _image_fs.get_mapper("https://thewtex.github.io/allen-ccf-itk-vtk-zarr/average_template_50_chunked.zarr")
_image_store_cached = zarr.LRUStoreCache(_image_store, max_size=None)
_image_ds = xr.open_zarr(_image_store_cached, consolidated=True)
_image_da = _image_ds.average_template_50

class CCFWidget(Widget):
    """A Jupyter widget for the Allen Common Coordinate Framework (CCF)
    Mouse Brain Atlas."""

    def __init__(self, **kwargs):
        self._image = itk.image_from_xarray(_image_da)
        print(self._image)

        super(CCFWidget, self).__init__(**kwargs)
