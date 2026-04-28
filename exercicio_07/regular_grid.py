import geopandas as gpd
from shapely.geometry import Polygon
import numpy as np
import os


def create_grid(bounds, cell_size, crs='EPSG:3857'):

    # Limites da área de interesse
    minx, miny, maxx, maxy = bounds

    # Calcular número de células em x e y
    width = maxx - minx
    height = maxy - miny
    n_cells_x = int(np.ceil(width / cell_size))
    n_cells_y = int(np.ceil(height / cell_size))

    # Criar lista de polígonos
    polygons = []
    for i in range(n_cells_x):
        for j in range(n_cells_y):
            x1 = minx + i * cell_size
            y1 = miny + j * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            poly = Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])
            polygons.append(poly)

    # Criar GeoDataFrame
    gdf = gpd.GeoDataFrame({'geometry': polygons}, crs=crs)

    return gdf

def tile_by_grid(gdf, grid, output_dir='exercicio_07/tiles'):

    # Garantir CRS consistente
    if gdf.crs != grid.crs:
        gdf = gdf.to_crs(grid.crs)

    # Para cada célula do grid
    for idx, cell in grid.iterrows():
        # Recortar gdf pela célula usando interseção
        clipped = gpd.overlay(gdf, gpd.GeoDataFrame({'geometry': [cell.geometry]}, crs=grid.crs), how='intersection')

        # Só salva se houver feições
        if not clipped.empty:
            # Nome do arquivo baseado no índice
            filename = f'tile_{idx}.shp'
            filepath = os.path.join(output_dir, filename)

            # Salvando
            clipped.to_file(filepath)
    
    return


if __name__ == "__main__":

    # Create grid ======================================================================

    # Definindo área de interesse
    bounds = (0, 0, 10000, 10000)  # minx, miny, maxx, maxy
    cell_size = 1000

    # Criando grid
    grid = create_grid(bounds, cell_size)

    # Salvando arquivo
    grid.to_file('exercicio_07/grids/grid.shp')

    # Tile by grid =====================================================================

    # Criando GeoDataFrame de exemplo para testar tile_by_grid
    example_polygons = [
        Polygon([(1000, 1000), (2000, 1000), (2000, 2000), (1000, 2000)]),
        Polygon([(4500, 4500), (5500, 4500), (5500, 5500), (4500, 5500)]),
        Polygon([(2100, 2500), (3300, 2000), (3100, 3200), (2200, 4500), (2100, 2500)]),
    ]
    example_gdf = gpd.GeoDataFrame({
        'id': [1, 2, 3],
        'name': ['area1', 'area2', 'area3'],
        'geometry': example_polygons
    }, crs='EPSG:3857')

    # Aplicando tile_by_grid
    tile_by_grid(example_gdf, grid, 'exercicio_07/tiles')
