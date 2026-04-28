import rasterio
import os
import json
from pathlib import Path


def inspect_raster(raster_path):
    with rasterio.open(raster_path) as src:
        # Extração de metadados
        crs = src.crs
        gsd = src.res
        bounds = src.bounds
        count = src.count
        dtype = src.meta['dtype']
        nodata = src.meta['nodata']

        # Dict para criar arquivo JSON
        data = {
            'crs': str(crs),
            'gsd': tuple(gsd),
            'bounds': tuple(bounds),
            'count': int(count),
            'dtype': str(dtype),
            'nodata': None if nodata is None else 
            (int(nodata) if isinstance(nodata, (int,)) else float(nodata))
        }

    return data


if __name__ == "__main__":
    # Dict para consolidar todos os rasters
    all_data = dict()

    # Preenchendo o dict
    dir = Path('exercicio_02/raster_inspection')
    for raster_file in dir.glob('*.tif'):
        all_data[raster_file.name] = inspect_raster(raster_file)

    # Exportando JSON
    json_output = os.path.join(dir, 'raster_inspection.json')
    with open(json_output, 'w') as f:
        json.dump(all_data, f,  indent=4)
