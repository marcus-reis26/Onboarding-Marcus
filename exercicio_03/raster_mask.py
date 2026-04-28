import rasterio
import numpy as np
import os
from pathlib import Path


def mask_raster_by_threshold(raster_path, threshold, output_path, band=1):

    with rasterio.open(raster_path) as src:
        # Leitura da banda especificada
        data = src.read(band) if band <= src.count else src.read(1)
        nodata = src.nodata

        # Criação da máscara binária
        if nodata is not None:
            mask_bin = np.where(data == nodata, 0, (data > threshold).astype(np.uint8))
        else:
            mask_bin = (data > threshold).astype(np.uint8)

        # Cópia dos metadados e atualização para banda única
        profile = src.profile
        profile.update(
            dtype=rasterio.uint8,
            nodata=0,
            count=1
        )

        # Escrita do raster binário preservando CRS e transform
        with rasterio.open(output_path, 'w', **profile) as nsrc:
            nsrc.write(mask_bin, 1)


if __name__ == "__main__":
    dir_input = Path('exercicio_03/raster_inspection')
    dir_output = Path('exercicio_03/raster_masks')

    # Thresholds
    thresholds = {
        'Orthomosaico': 150,
        'MDS': 0.3,
        'Indice_GLI': 0.02
    }

    for raster_file in dir_input.glob('*.tif'):
        base_name = raster_file.stem
        threshold = thresholds.get(base_name, 100)  # Default 100

        output_file = os.path.join(dir_output, f"{base_name}_mask.tif")
        mask_raster_by_threshold(raster_file, threshold=threshold, output_path=output_file, band=1)
