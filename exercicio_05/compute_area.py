import geopandas as gpd


def add_polygon_area(gdf, col_name='area_ha'):
    gdf = gdf.to_crs(epsg=3857)  # CRS métrico
    gdf[col_name] = gdf.geometry.area / 10000  # Calculando área em ha
    gdf = gdf.to_crs(epsg=4326)  # Voltando para CRS geográfico
    
    print(gdf[[col_name]].head())  # Exibindo os primeiros valores da nova coluna
    
    return gdf


if __name__ == "__main__":

    add_polygon_area(gpd.read_file('exercicio_05/plantio_area.geojson'))