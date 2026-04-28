import geopandas as gpd
import os


def explode_multipart(gdf):

    gdf_exploded = gdf.explode(index_parts=False).reset_index(drop=True)
    
    print(gdf_exploded.head())  # Exibindo os primeiros valores do GeoDataFrame resultante
    
    return gdf_exploded


if __name__ == "__main__":
    
    gdf_exploded = explode_multipart(gpd.read_file('exercicio_05/plantio_area.geojson'))

    output_path = os.path.join('exercicio_05', 'plantio_area_exploded.geojson')
    gdf_exploded.to_file(output_path, driver='GeoJSON')
