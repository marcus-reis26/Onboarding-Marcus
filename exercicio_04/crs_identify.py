import geopandas as gpd
import numpy as np
from vectors_inspect import load_vector


def identify_utm_crs(gdf):
    # Assegurando CRS WGS84 para pegar longitude e latitude
    if gdf.crs != 'EPSG:4326':
        gdf = gdf.to_crs('EPSG:4326')

    centroids = gdf.geometry.centroid
    lons = centroids.x  # Longitudes
    lats = centroids.y  # Latitudes

    utm_zones = np.floor((lons + 180) / 6) + 1  # Cálculo da zona UTM

    hemispheres = np.where(lats >= 0, 'N', 'S')  # Determinação do hemisfério

    epsg_utms = np.where(lats >= 0, 32600 + utm_zones, 32700 + utm_zones)  # Códigos EPSG

    print(f'UTM Zones: {utm_zones}')
    print(f'Hemispheres: {hemispheres}')
    print(f'EPSG UTM Codes: {epsg_utms}')

    # Estimativa automática com geopandas
    utm_estimated = gdf.estimate_utm_crs()
    print(f"UTM estimado pelo GeoPandas: {utm_estimated}")


if __name__ == "__main__":
    # Carregar arquivo
    input_path = 'exercicio_04/MATOLOGIA_Orthomosaico.geojson'
    gdf = load_vector(input_path)

    # Identificar CRS UTM
    identify_utm_crs(gdf)
