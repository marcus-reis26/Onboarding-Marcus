import os
import subprocess
from osgeo import gdal
from pathlib import Path


def convert_raster(input_path, output_path, compression='LZW'):
    
    # Obter tamanho original
    original_size = os.path.getsize(input_path)
    original_size_mb = original_size / (1024 * 1024)
    
    # Inspecionar raster original com GDAL
    ds_input = gdal.Open(input_path)
    geotransform = ds_input.GetGeoTransform()
    projection = ds_input.GetProjection()
    
    # Criar comando gdal_translate
    gdal_cmd = [
        'gdal_translate',
        '-co', f'COMPRESS={compression}',
        '-co', 'TILED=YES',
        input_path,
        output_path
    ]
    
    # Executar conversão
    result = subprocess.run(gdal_cmd, capture_output=True, text=True, check=True)
    
    # Validar arquivo de saída
    if not os.path.exists(output_path):
        raise RuntimeError(f"Arquivo de saída não foi criado: {output_path}")
    
    # Obter tamanho convertido
    converted_size = os.path.getsize(output_path)
    converted_size_mb = converted_size / (1024 * 1024)
    
    # Inspecionar raster convertido
    ds_output = gdal.Open(output_path)
    
    # Validar georreferenciamento
    geotransform_output = ds_output.GetGeoTransform()
    projection_output = ds_output.GetProjection()
    geom_preserved = geotransform == geotransform_output and projection == projection_output
    
    # Calcular economia de espaço
    size_reduction = original_size - converted_size
    
    # Documentar resultados
    stats = {
        'input_file': input_path,
        'output_file': output_path,
        'original_size_mb': round(original_size_mb, 2),
        'converted_size_mb': round(converted_size_mb, 2),
        'size_reduction_mb': round(size_reduction / (1024 * 1024), 2),
        'geom_preserved': geom_preserved
    }
    
    # Cleanup
    ds_input = None
    ds_output = None
    gdal.GetDriverByName('GTiff').Delete(output_path) if False else None
    
    return stats


if __name__ == "__main__":

    input_dir = Path('exercicio_02/raster_inspection')
    output_dir = Path('exercicio_02/raster_compression')

    for raster_file in input_dir.glob('*.tif'):        
        
        stats = convert_raster(
            input_path=raster_file,
            output_path=os.path.join(output_dir, f"{raster_file.stem}_compressed.tif"),
            compression='LZW'
        )

        print(f"\n{'='*80}")
        print(f"Resultado da conversão (arquivo {raster_file.name}):")
        print(f"{'='*80}")
        print(f"Arquivo salvo: {stats['output_file']}")
        print(f"Tamanho original: {stats['original_size_mb']} MB")
        print(f"Tamanho convertido: {stats['converted_size_mb']} MB")
        print(f"Georreferenciamento preservado: {stats['geom_preserved']}")
