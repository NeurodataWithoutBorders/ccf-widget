import numpy as np

def swc_morphology_geometry(morphology):
    geometry = {'vtkClass': 'vtkPolyData'}

    number_of_points = len(morphology.compartment_list)

    point_ids = list(morphology.compartment_index.keys())
    point_ids.sort()

    points_data = np.zeros((number_of_points, 3), dtype=np.float32)

    verts_data = np.ones((2 * number_of_points,), dtype=np.uint32)
    verts_data[1::2] = np.arange(number_of_points, dtype=np.uint32)

    lines_data = []
    # radius
    point_data = np.zeros((number_of_points,), dtype=np.float32)
    for index, compartment in enumerate(morphology.compartment_list):
        # Assume sorted by id
        point_index = point_ids.index(compartment['id'])
        points_data[index, 0] = compartment['x']
        points_data[index, 1] = compartment['y']
        points_data[index, 2] = compartment['z']

        point_data[index] = compartment['radius']
        if compartment['type'] == 0:
            # unknown
            pass
        else:
            # soma, axon, basal dendrite, or apical dendrite
            for child in compartment['children']:
                child_index = point_ids.index(morphology.compartment_index[child]['id'])
                lines_data.extend([2, point_index, child_index])
    lines_data = np.array(lines_data, dtype=np.uint32)

    points = {'vtkClass': 'vtkPoints',
              'name': 'swc_morphology',
              'numberOfComponents': 3,
              'dataType': 'Float32Array',
              'size': points_data.size,
              'values': points_data}
    geometry['points'] = points
    pd = { 'vtkClass': 'vtkDataSetAttributes',
         'activeScalars': 0,
         'arrays': [{'data': {'vtkClass': 'vtkDataArray',
                              'name': 'Radius',
                              'numberOfComponents': 1,
                              'size': point_data.size,
                              'dataType': 'Float32Array',
                              'values': point_data }}]}
    geometry['pointData'] = pd
    for cell_type, cell_data in [('verts', verts_data), ('lines', lines_data)]:
        cells = {'vtkClass': 'vtkCellArray',
                 'name': '_' + cell_type,
                 'numberOfComponents': 1,
                 'size': cell_data.size,
                 'dataType': 'Uint32Array',
                 'values': cell_data}
        geometry[cell_type] = cells

    soma = morphology.soma
    soma_point = [soma['x'], soma['y'], soma['z']]
    soma_point = np.asarray(soma_point).astype(np.float32).reshape((1,3))

    return (soma_point, geometry)
