import zarr
from fsspec.implementations.http import HTTPFileSystem
from itkwidgets._transform_types import zarr_to_vtkjs

_cache = dict()

def structure_mesh(allen_id):
    if allen_id in _cache:
        return _cache[allen_id]
    fs = HTTPFileSystem()
    # Todo: Use AWS store after Scott / Lydia upload
    store = fs.get_mapper("https://thewtex.github.io/allen-ccf-itk-vtk-zarr/meshes/{0}.zarr".format(allen_id))
    root = zarr.open_consolidated(store)
    mesh = zarr_to_vtkjs(root)
    _cache[allen_id] = mesh
    return mesh
