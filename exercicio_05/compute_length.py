import geopandas as gpd


def add_linestring_length(gdf, col_name="length_m"):
    
    gdf = gdf.to_crs(epsg=3857)  # CRS métrico
    gdf[col_name] = gdf.geometry.length  # Calculando comprimento
    gdf = gdf.to_crs(epsg=4326)  # Voltando para CRS geográfico
    
    print(gdf[[col_name]].head())  # Exibindo os primeiros valores da nova coluna
    
    return gdf


if __name__ == "__main__":

    add_linestring_length(gpd.read_file('exercicio_05/LINHAS.geojson'))
