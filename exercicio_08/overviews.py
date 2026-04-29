from osgeo import gdal


def build_overviews(raster_path):

    dataset = gdal.Open(raster_path, gdal.GA_Update)
    if dataset is None:
        raise ValueError(f'Não foi possível abrir o arquivo raster: {raster_path}')

    overview_levels = [2, 4, 8, 16, 32]
    dataset.BuildOverviews('NEAREST', overview_levels)
    dataset.FlushCache()
    dataset = None


if __name__ == '__main__':
    raster_path = 'exercicio_08/overviews/Orthomosaico.gpkg'
    build_overviews(raster_path)
