import geopandas as gpd


def fix_invalid_geometries(gdf):
    """
    Detecta e corrige geometrias inválidas em um GeoDataFrame.
    Retorna o GeoDataFrame corrigido e os totais de inválidas antes/depois.
    """
    gdf = gdf.copy()
    invalid_before = int((~gdf.geometry.is_valid).sum())

    if invalid_before > 0:
        # Tentando buffer(0) primeiro
        gdf.loc[~gdf.geometry.is_valid, 'geometry'] = (
            gdf.loc[~gdf.geometry.is_valid, 'geometry'].buffer(0)
        )

        # Para as que ainda são inválidas, tentando make_valid()
        still_invalid = ~gdf.geometry.is_valid
        if still_invalid.any():
            try:
                gdf.loc[still_invalid, 'geometry'] = (
                    gdf.loc[still_invalid, 'geometry'].make_valid()
                )
            except Exception as e:
                print(f"Aviso: make_valid() falhou: {e}")

    invalid_after = int((~gdf.geometry.is_valid).sum())

    return gdf, invalid_before, invalid_after


if __name__ == '__main__':

    path = 'exercicio_05/plantio_area.geojson'
    output_path = 'exercicio_05/plantio_area_fixed.geojson'

    gdf = gpd.read_file(path)

    fixed_gdf, invalid_before, invalid_after = fix_invalid_geometries(gdf)
    fixed_gdf.to_file(output_path, driver='GeoJSON')

    print('Inválidas detectadas:', invalid_before)
    print('Inválidas após correção:', invalid_after)
