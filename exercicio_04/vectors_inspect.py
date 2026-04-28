import geopandas as gpd


def load_vector(path):

    gdf = gpd.read_file(path)

    # get CRS
    crs = gdf.crs

    # get geometry type
    geom_type = gdf.geom_type
    uq_geom_type = gdf.geom_type.unique()

    # get column names
    cols = gdf.columns

    # get data types
    dtypes = gdf.dtypes

    print(f'='*60)
    print('Inspeção do vetor:')
    print(f'='*60)
    print(f'crs: {crs}')
    print(f'geometry type: {geom_type}')
    print(f'unique geometry types: {uq_geom_type}')
    print(f'column names: {cols}')
    print(f'data types: {dtypes}')

    return gdf


if __name__ == "__main__":
    # Carregar arquivo
    input_path = 'exercicio_04/MATOLOGIA_Orthomosaico.geojson'
    gdf = load_vector(input_path)
