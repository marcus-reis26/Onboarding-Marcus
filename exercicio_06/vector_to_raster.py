import math
import geopandas as gpd
import rasterio
from rasterio.features import rasterize
from rasterio.transform import from_origin


def rasterize_vector(
    vector_path,
    output_path,
    attribute=None,
    pixel_size=10,
    burn_value=1,
    nodata=0,
    dtype='uint8',
):

    gdf = gpd.read_file(vector_path)

    minx, miny, maxx, maxy = gdf.total_bounds
    width = math.ceil((maxx - minx) / pixel_size)
    height = math.ceil((maxy - miny) / pixel_size)
    transform = from_origin(minx, maxy, pixel_size, pixel_size)

    if attribute is not None:
        if attribute not in gdf.columns:
            raise ValueError(f'Atributo "{attribute}" não encontrado no vetor.')
        shapes = ((geom, int(value)) for geom, value in zip(gdf.geometry, gdf[attribute]))
    else:
        shapes = ((geom, burn_value) for geom in gdf.geometry)

    raster_profile = {
        'driver': 'GTiff',
        'height': height,
        'width': width,
        'count': 1,
        'dtype': dtype,
        'crs': gdf.crs,
        'transform': transform,
        'nodata': nodata,
        'compress': 'lzw',
    }

    with rasterio.open(output_path, 'w', **raster_profile) as dst:
        burned = rasterize(
            shapes,
            out_shape=(height, width),
            transform=transform,
            fill=nodata,
            dtype=dtype,
            default_value=burn_value,
            all_touched=False,
        )
        dst.write(burned, 1)


if __name__ == '__main__':
    vector_path = 'exercicio_06/output.geojson'
    output_path = 'exercicio_06/vectorized.tif'
    rasterize_vector(
        vector_path,
        output_path,
        attribute=None,
        pixel_size=.03,
        burn_value=1,
        nodata=0,
        dtype='uint8',
    )
