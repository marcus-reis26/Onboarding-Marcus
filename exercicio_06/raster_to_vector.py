import rasterio
import geopandas as gpd
from rasterio.features import shapes
from osgeo import gdal
import subprocess


def polygonize_raster_rasterio(raster_path, output_path):

    with rasterio.open(raster_path) as src:
        band = src.read(1)  # Lê a banda 1
        transform = src.transform
        crs = src.crs
        mask = band == 1  # Considera pixels == 1 como parte do polígono

        # Polygonizando
        results = (
            {'properties': {'raster_val': v}, 'geometry': s}
            for _, (s, v) in enumerate(
                shapes(band, mask=mask, transform=transform)
            )
        )
        polygons = list(results)

        gdf = gpd.GeoDataFrame.from_features(polygons, crs=crs)  # Criando GeoDataFrame
        gdf.to_file(output_path, driver='GeoJSON')


def polygonize_raster(raster_path, output_path):

    # Com rasterio
    # polygonize_raster_rasterio(raster_path, output_path)

    # Com o comando gdal_polygonize.py
    gdal_cmd = [
        'gdal_polygonize.py',
        raster_path,
        '-f', "GeoJSON",
        output_path
    ]
    subprocess.run(gdal_cmd, capture_output=True, text=True, check=True)

if __name__ == "__main__":
    raster_path = 'exercicio_06/rasters/Indice_GLI.tif'
    output_path = 'exercicio_06/MDS_polygons.geojson'
    polygonize_raster(raster_path, output_path)
