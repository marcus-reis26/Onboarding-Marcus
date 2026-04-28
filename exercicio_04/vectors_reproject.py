import geopandas as gpd
import os
from vectors_inspect import load_vector


def reproject_gdf(gdf, target_epsg):
    """Reprojeta um GeoDataFrame para um sistema de referência de coordenadas (CRS) diferente."""
    
    if gdf.crs is None:
        raise ValueError("O GeoDataFrame deve ter um CRS definido para reprojetar.")
    
    return gdf.to_crs(target_epsg)


if __name__ == "__main__":

    # Carregando arquivo
    input_path = 'exercicio_04/MATOLOGIA_Orthomosaico.geojson'
    gdf = load_vector(input_path)

    # Reprojetando para EPSG:3857
    reprojected_gdf = reproject_gdf(gdf, 'EPSG:3857')

    # Exportando arquivo
    output_dir = 'exercicio_04/reprojected_vector'
    output_path = os.path.join(output_dir, 'MATOLOGIA_Orthomosaico_EPSG3857.geojson')
    reprojected_gdf.to_file(output_path, driver='GeoJSON')
