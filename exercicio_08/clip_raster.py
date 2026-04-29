import rasterio
from rasterio.windows import Window
from osgeo import gdal


def clip_raster_bbox(raster_path, bbox, output_path_window, output_path_gdal):

    # Usando rasterio.windows ==============================================
    window = Window(bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1])

    with rasterio.open(raster_path) as src:
        data = src.read(window=window)
        print(src.crs)
        transform = src.transform
        new_transform = src.window_transform(window)
        profile = src.profile
        profile.update({
            'height': window.height,
            'width': window.width,
            'transform': new_transform
        })
    
    with rasterio.open(output_path_window, 'w', **profile) as dst:
        dst.write(data)

    # Usando GDAL =========================================================
    ds = gdal.Open(raster_path)
    if ds is None:
        raise ValueError(f'Não foi possível abrir o arquivo raster: {raster_path}')
    
    left, top = transform * (bbox[0], bbox[1])  # (px_min, py_min)
    right, bottom = transform * (bbox[2], bbox[3])  # (px_max, py_max)
    
    gdal.Translate(
        output_path_gdal,
        ds,
        projWin=(left, top, right, bottom)
    )

    ds = None


if __name__ == '__main__':

    raster_path = 'exercicio_08/bbox/Orthomosaico.tif'
    output_path_window = 'exercicio_08/bbox/clipped_by_window.tif'
    output_path_gdal = 'exercicio_08/bbox/clipped_by_gdal.tif'

    bbox = (1000, 1000, 3000, 4000)  # (px_min, py_min, px_max, py_max)
    clip_raster_bbox(raster_path, bbox, output_path_window, output_path_gdal)
