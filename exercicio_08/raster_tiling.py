import os
import rasterio
from rasterio.mask import mask
from regular_grid import create_grid


def tile_raster(raster_path, tile_size, output_dir):

    with rasterio.open(raster_path) as src:
        crs = src.crs
        profile = src.profile

        # Garantindo CRS em metros
        if not crs.is_projected:
            src = src.to_crs('EPSG:31983')

        # Criando grid
        bounds = (683650, 8227460, 683780, 8227600)  # minx, miny, maxx, maxy
        cell_size = tile_size
        grid = create_grid(bounds, cell_size, crs=crs)
        grid.to_file('exercicio_08/grid/grid.shp')

        # Para cada célula do grid
        for idx, cell in grid.iterrows():
            # Converter geometria para formato compatível com rasterio.mask
            shapes = [cell.geometry]
            
            try:
                # Clipar raster pela célula
                clipped_array, clipped_transform = mask(
                    src,
                    shapes,
                    crop=True,
                    nodata=src.nodata
                )
                
                if clipped_array.size > 0:
                    # Atualizar perfil com novos parâmetros
                    clipped_profile = profile.copy()
                    clipped_profile.update({
                        'height': clipped_array.shape[1],
                        'width': clipped_array.shape[2],
                        'transform': clipped_transform
                    })
                    
                    # Salvando
                    filename = f'tile_{idx + 1}.tif'
                    filepath = os.path.join(output_dir, filename)
                    
                    with rasterio.open(filepath, 'w', **clipped_profile) as dst:
                        dst.write(clipped_array)
            
            except ValueError:
                # Célula fora dos limites do raster
                continue


if __name__ == "__main__":

    raster_path = 'exercicio_08/bbox/Orthomosaico.tif'
    tile_size = 10  # [m]
    output_dir = 'exercicio_08/tiles'

    tile_raster(raster_path, tile_size, output_dir)
