import rasterio
import numpy as np
import os
import json
from pathlib import Path


def raster_band_stats(raster_path):

    with rasterio.open(raster_path) as src:
        stats_automatic = None
        stats_compared = {}

        for k in range(1, src.count + 1):
            # Lendo a banda
            band = src.read(k).astype(np.float32)

            # Ignorando nodata explicitamente
            nodata = src.nodata
            if nodata is not None:
                mask = band != nodata
                valid_pixels = band[mask]
            else:
                valid_pixels = band.flatten()

            stats_automatic = src.statistics(k)  # Cálculo automático
            
            # Comparação de cálculos em um dict
            stats_compared[f'band_{k}'] = {
                'min_manual': float(np.min(valid_pixels)),
                'min_automatic': stats_automatic.min,
                'max_manual': float(np.max(valid_pixels)),
                'max_automatic': stats_automatic.max,
                'mean_manual': float(np.mean(valid_pixels)),
                'mean_automatic': stats_automatic.mean,
                'std_manual': float(np.std(valid_pixels)),
                'std_automatic': stats_automatic.std
            }
    
    return stats_compared


if __name__ == "__main__":
    
    # Dict para consolidar todos os rasters
    all_data = dict()

    # Preenchendo o dict
    dir = Path('exercicio_03/raster_inspection')
    for raster_file in dir.glob('*.tif'):
        all_data[raster_file.name] = raster_band_stats(raster_file)

    # Exportando JSON
    json_output = os.path.join(dir, 'raster_stats.json')
    with open(json_output, 'w') as f:
        json.dump(all_data, f,  indent=4)

    # Os valores calculados diferem bastante nos canais RGB.
